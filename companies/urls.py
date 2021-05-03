from django.urls import path

from .views      import NotificationView,TagView,NotificationDetailView,NotificationLikeView

urlpatterns = [
    path('',NotificationView.as_view()),
    path('/tag',TagView.as_view()),
    path('/<int:notification_id>',NotificationDetailView.as_view()),
    path('/like',NotificationLikeView.as_view())
]