from django.urls import path

from .views import NotificationView,TagView

urlpatterns = [
    path('',NotificationView.as_view()),
    path('/tag',TagView.as_view())
]