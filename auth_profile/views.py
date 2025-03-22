from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from auth_profile.serializers import UserSerializer, UserCodeCheckingSerializer
from auth_profile.models import User



class UserSignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserChecking(CreateAPIView):
    serializer_class = UserCodeCheckingSerializer


    def create(self, request: Request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            data = ser.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(ser.error, status=status.HTTP_400_BAD_REQUEST)
