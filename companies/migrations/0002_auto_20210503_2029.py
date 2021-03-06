# Generated by Django 3.1.7 on 2021-05-03 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_merge_20210503_1814'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'likes',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ManyToManyField(related_name='userlike', through='companies.Like', to='users.User'),
        ),
    ]
