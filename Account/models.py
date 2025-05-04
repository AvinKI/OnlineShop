from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11 , blank=False)
    address = models.CharField(max_length=200 , null=True)
    email = models.EmailField( null=True , blank=True , unique=True )
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"