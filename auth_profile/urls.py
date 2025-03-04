from django.urls import path

from auth_profile.views import UserSignUp, UserChecking

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('verify/', UserChecking.as_view(), name='verify'),
]

