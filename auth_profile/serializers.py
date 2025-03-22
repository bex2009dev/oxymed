from rest_framework import serializers
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken


from auth_profile.tasks import user_email_message
from auth_profile.models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, write_only=True)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    fathers_name = serializers.CharField(max_length=200, required=False)
    birthday = serializers.DateTimeField(read_only=True)
    image = serializers.FileField(required=False)

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if not user is None:
            if user.is_active == False:
                user_email_message.delay(email=user.email)
                return user
            raise serializers.ValidationError({"error": "You should signin !!!"})
        else:
            user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
            user_email_message.delay(email=user.email)
            
            return user
    

class UserCodeCheckingSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=15)

    def create(self, validated_data):
        try:
            email = validated_data.get('email')
            code = validated_data.get('code')
            user = User.objects.get(email=email)
            if code == cache.get(email):
                user.is_active = True
                user.save()
                cache.delete(email)
                token = RefreshToken.for_user(user=user)
                return {
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                }
            return {"message": "Code is incorrect !!!"}
        except:
            raise ValueError('Email is wrong !!!')
        

# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2OTU0MDg3LCJpYXQiOjE3NDI2MzQwODcsImp0aSI6ImY3MmYxOTgxZjE1NzQzNTliNmY1MDI2YTg3NzYzMGVjIiwidXNlcl9pZCI6MTZ9.76eXhTA8RnTX7C6A-b-GTMW4GIWARYg2KyOzhVL5u4Y",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTI3NDA4NywiaWF0IjoxNzQyNjM0MDg3LCJqdGkiOiJjODBlY2Y5YmI0NWE0MjVhODQwZmZiYTI2MWY2MWM3MyIsInVzZXJfaWQiOjE2fQ.Jndji7_nLBtPtLTMatn7IkRCKxo0AVxstSWCSEll__k"
# }