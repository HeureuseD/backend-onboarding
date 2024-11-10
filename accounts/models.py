from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+\-\s]+$',  
                message='Username may contain letters, numbers, @/./+/-/_ characters, and spaces.'
            ),
        ]
    )
    nickname = models.CharField(max_length=30, unique=True)