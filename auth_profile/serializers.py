from rest_framework.serializers import ModelSerializer

from auth_profile.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    
    def create(self, validated_data):
        return super().create(validated_data)