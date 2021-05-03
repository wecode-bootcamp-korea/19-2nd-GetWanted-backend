from django.db import models
 
class Notification(models.Model):
    title       = models.CharField(max_length=45)
    description = models.TextField()
    company     = models.ForeignKey('Company',on_delete=models.CASCADE)
    tag         = models.ManyToManyField('Tag',through='NotificationTag')
    user        = models.ManyToManyField('users.User', through='Like', related_name='userlike')
    class Meta:
        db_table = 'notifications'

class Image(models.Model):
    image_url    = models.URLField()
    notification = models.ForeignKey('Notification',on_delete=models.CASCADE)
    class Meta:
        db_table = 'images'

class Company(models.Model):
    name      = models.CharField(max_length=45)
    address   = models.CharField(max_length=500)
    latitude  = models.DecimalField(max_digits=20, decimal_places=10)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)
    class Meta:
        db_table = 'companies'

class Tag(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'tags'

class NotificationTag(models.Model):
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    tag          = models.ForeignKey('Tag', on_delete=models.CASCADE)
    class Meta:
        db_table = 'notification_tags'

class Like(models.Model):
    notification = models.ForeignKey('Notification',on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE)
    is_liked     = models.BooleanField()

    class Meta:
        db_table = 'likes'