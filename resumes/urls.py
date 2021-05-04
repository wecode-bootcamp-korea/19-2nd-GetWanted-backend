from django.urls import path

from .views      import ResumeView,ResumeListView

urlpatterns = [
    path('/<int:resume_id>', ResumeView.as_view()),
    path('', ResumeView.as_view()),
    path('/lists',ResumeListView.as_view())
]