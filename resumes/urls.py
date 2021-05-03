from django.urls import path
from .views      import ResumeView
urlpatterns = [
    path('/<int:resume_id>', ResumeView.as_view()),
    path('', ResumeView.as_view())
]