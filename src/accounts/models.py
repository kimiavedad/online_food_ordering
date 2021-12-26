from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Site Admin', 'Site Admin'),
        ('Restaurant Manager', 'Restaurant Manager'),
        ('Customer', 'Customer'),
    ]
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)
    address = models.ManyToManyField('Address', blank=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        return self.device


class Customer(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Customer'


class RestaurantManager(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Restaurant Manager'


class SiteAdmin(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Site Admin'


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    plaque = models.PositiveIntegerField()

