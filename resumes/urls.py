from django.urls import path

from .views import ResumeView,ResumeListView,FileResumeView

urlpatterns = [
    path('/files/<int:resume_id>', FileResumeView.as_view()),
    path('/files', FileResumeView.as_view()),
    path('/<int:resume_id>', ResumeView.as_view()),
    path('', ResumeView.as_view()),
    path('/lists', ResumeListView.as_view())
]