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
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.fathers_name = validated_data.get('fathers_name', instance.fathers_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.image = validated_data.get('image', instance.image)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()

        return instance
    

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
                tokens = RefreshToken.for_user(user)
                return {
                    "access_token": str(tokens.access_token),
                    "refresh_token": str(tokens),
                }
            return {"message": "Code is incorrect !!!"}
        except:
            raise ValueError('Email is wrong !!!')
        

class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, write_only=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            return {'error': 'User with such email does not exist!!!'}
        
        if user.check_password(raw_password=password):
            tokens = RefreshToken.for_user(user)

            return {
                "access_token": str(tokens.access_token),
                "refresh_token": str(tokens),
            } 
        
        else:
            return {'error': 'Password is incorrect!!!'}