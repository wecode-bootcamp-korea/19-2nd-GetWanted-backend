from django.db import models

class Resume(models.Model):
    title        = models.CharField(max_length=50)
    name         = models.CharField(max_length=50)
    email        = models.EmailField()
    phone_number = models.CharField(max_length=20)
    introduction = models.TextField()
    status       = models.BooleanField(default=0)
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'resumes'

class Career(models.Model):
    is_working    = models.BooleanField(default=0)
    start_working = models.CharField(max_length=50)
    end_working   = models.CharField(max_length=50)
    company_name  = models.CharField(max_length=45)
    department    = models.CharField(max_length=45)
    description   = models.TextField()
    resume        = models.ForeignKey('Resume', on_delete=models.CASCADE)
    class Meta:
        db_table = 'careers'

class FileResume(models.Model):
    file_url   = models.URLField()
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'file_resumes'