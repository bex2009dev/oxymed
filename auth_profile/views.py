from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from auth_profile.serializers import UserSerializer, UserCodeCheckingSerializer, UserSignInSerializer
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


class UserSignIn(GenericAPIView):
    serializer_class = UserSignInSerializer


    def post(self, request: Request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        print(request.data)
        if ser.is_valid(raise_exception=True): 
            data = ser.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(ser.error, status=status.HTTP_400_BAD_REQUEST)


class UserInfoEdit(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user