from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name' ,'username']

