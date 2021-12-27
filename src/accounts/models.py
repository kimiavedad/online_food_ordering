from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('مدیر سایت', 'مدیر سایت'),
        ('مدیر رستوران', 'مدیر رستوران'),
        ('مشتری', 'مشتری'),
    ]
    email = models.EmailField()
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


class RestaurantManager(CustomUser):
    class Meta:
        proxy = True


class SiteAdmin(CustomUser):
    class Meta:
        proxy = True


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    plaque = models.PositiveIntegerField()

    def __str__(self):
        return self.city + " - " + self.street
