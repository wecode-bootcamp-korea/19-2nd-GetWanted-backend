# Generated by Django 3.1.7 on 2021-05-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20210503_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='is_liked',
            field=models.BooleanField(),
            preserve_default=False,
        ),
    ]