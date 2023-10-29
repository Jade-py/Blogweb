from django.db import models
from datetime import datetime, date
from tinymce.models import HTMLField
from users.models import CustomUser

# Create your models here.


class Dashboard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')
    Monday = models.DateTimeField(default=datetime.min)
    Tuesday = models.DateTimeField(default=datetime.min)
    Wednesday = models.DateTimeField(default=datetime.min)
    Thursday = models.DateTimeField(default=datetime.min)
    Friday = models.DateTimeField(default=datetime.min)
    Saturday = models.DateTimeField(default=datetime.min)
    Sunday = models.DateTimeField(default=datetime.min)


class Notes(models.Model):
    title = models.CharField(max_length=2000)
    explanation = models.TextField()
    content = HTMLField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')
    saved = models.DateTimeField(default=datetime.min)


class Storage(models.Model):
    file = models.FileField(upload_to='storage/')
    folder = models.TextField(default=' ')
    upload_time = models.DateTimeField(default=datetime.min)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')


class Calendar(models.Model):
    start_date = models.DateField(default=date.min)
    end_date = models.DateField(default=date.min)
    event = models.TextField(null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')


class Todo(models.Model):
    task = models.TextField(null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')


class Deadlines(models.Model):
    task = models.TextField(null=True)
    ended_on = models.DateField(default=date.today())
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')


class RecentWorks(models.Model):
    item = models.TextField(null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='anonymous')

