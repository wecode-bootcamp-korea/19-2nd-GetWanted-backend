from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    phonenumber  = models.CharField(max_length=45)
    password     = models.CharField(max_length=500)
    is_social    = models.BooleanField(default=0)
    email        = models.EmailField()
    position     = models.ForeignKey('Position',on_delete=models.PROTECT)
    notification = models.ManyToManyField('companies.Notification', through='ApplyList')
    class Meta:
        db_table = 'users'

class Position(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'positions'

class ApplyList(models.Model):
    notification = models.ForeignKey('companies.Notification',on_delete=models.CASCADE)
    user         = models.ForeignKey('User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'apply_lists'