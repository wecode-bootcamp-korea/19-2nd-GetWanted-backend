from django.urls import path
from users.views import SignUpView, EmailCheckView, SignInView

urlpatterns = [
        path('/signup', SignUpView.as_view()),
        path('/email', EmailCheckView.as_view()),
        path('/signin', SignInView.as_view())
        ]
