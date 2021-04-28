from django.urls import path

from .views import NotificationlistView

urlpatterns = [
    path('',NotificationlistView.as_view())
]
