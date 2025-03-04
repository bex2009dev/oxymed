from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from random import randint

from auth_profile.models import User


signup_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="User email"),
        'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description="User password"),
    },
)


verify_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'code'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="User email"),
        'code': openapi.Schema(type=openapi.TYPE_STRING, description="Verification code"),
    },
)


class UserSignUp(APIView):
    @swagger_auto_schema(request_body=signup_schema)
    def post(self, req: Request):
        email = req.data.get('email')
        password = req.data.get('password')
        code = str(randint(1000, 9000))

        if email is None or password is None:
            print(email, password)
            return Response({'error': 'Email or password is incorrect !!!'}, status=status.HTTP_400_BAD_REQUEST)
        
        send_mail("OXYmed", f'Your code is {code}', settings.EMAIL_HOST_USER, [email])
        user = User.objects.create_user(email=email, password=password)
        cache.set(str(user.email), code)

        return Response({'anwer': 'Check your email, and write code !!!'}, status=status.HTTP_201_CREATED)




class UserChecking(APIView):
    @swagger_auto_schema(request_body=verify_schema)
    def post(self, req: Request):
        email = req.data.get('email')
        code = req.data.get('code')

        if str(code) == cache.get(email):
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            cache.delete(email)

        token = RefreshToken.for_user(user=user)

        return Response({
            "refresh_token": str(token),
            "access_token": str(token.access_token), 
        })

