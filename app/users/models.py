from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User Model """
    phone = models.CharField(max_length=140, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
