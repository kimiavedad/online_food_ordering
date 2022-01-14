from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SITE_ADMIN = 'ادمین سایت', 'ادمین سایت'
        RESTAURANT_MANAGER = 'مدیر رستوران', 'مدیر رستوران'
        CUSTOMER = 'مشتری', 'مشتری'

    email = models.EmailField()
    device = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(choices=Role.choices, max_length=20, default=Role.SITE_ADMIN)

    def __str__(self):
        return self.email


class Customer(CustomUser):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CustomUser.Role.CUSTOMER
        return super().save(*args, **kwargs)


class RestaurantManager(CustomUser):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = CustomUser.Role.RESTAURANT_MANAGER
        self.is_staff = True
        return super().save(*args, **kwargs)


class SiteAdmin(CustomUser):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CustomUser.Role.SITE_ADMIN
            self.is_superuser = True
        return super().save(*args, **kwargs)


class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    plaque = models.PositiveIntegerField()
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.city + " - " + self.street
