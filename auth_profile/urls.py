from django.urls import path

from auth_profile.views import UserSignUp, UserChecking, UserSignIn, UserInfoEdit

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('verify/', UserChecking.as_view(), name='verify'),
    path('signin/', UserSignIn.as_view(), name='signin'),
    path('edit/', UserInfoEdit.as_view(), name='edit'),
]

