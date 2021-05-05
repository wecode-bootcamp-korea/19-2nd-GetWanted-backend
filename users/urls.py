from django.urls import path
from users.views import SignUpView, EmailCheckView, SignInView, KakaoSignin, GoogleSignin, NaverSignin, ResetPassword

urlpatterns = [
        path('/signup', SignUpView.as_view()),
        path('/email', EmailCheckView.as_view()),
        path('/signin', SignInView.as_view()),
        path('/kakao', KakaoSignin.as_view()),
        path('/google', GoogleSignin.as_view()),
        path('/naver', NaverSignin.as_view()),
        path('/reset', ResetPassword.as_view()),
        ]
