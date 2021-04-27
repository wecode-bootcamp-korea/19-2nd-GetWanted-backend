from django.db import models

class Resume(models.Model):
    introduction = models.TextField()
    status       = models.BooleanField(default=0)
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'resumes'

class Career(models.Model):
    is_working   = models.BooleanField(default=0)
    period       = models.DateField()
    company_name = models.CharField(max_length=45)
    department   = models.CharField(max_length=45)
    description  = models.TextField()
    resume       = models.ForeignKey('Resume', on_delete=models.CASCADE)
    class Meta:
        db_table = 'careers'

class FileResume(models.Model):
    file_url   = models.URLField()
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'file_resumes'