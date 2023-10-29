from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, primary_key=True, unique=True)
    last_logout = models.DateTimeField(null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('notes', args=(self.pk,))


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="Anonymous")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    college_name = models.TextField(max_length=250, default='Not Specified')
    stream = models.TextField(max_length=100, default='Not Specified')
    graduation_year = models.IntegerField(default=0)
    phone_no = PhoneNumberField('IN')

    def get_absolute_url(self):
        return reverse(self.pk)

# Create your models here.
