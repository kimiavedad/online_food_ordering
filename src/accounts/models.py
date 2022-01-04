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
    addresses = models.ManyToManyField('Address', blank=True, through='UserAddress')

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
        if not self.pk:
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
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    plaque = models.PositiveIntegerField()
    primary = models.BooleanField(null=True)

    def __str__(self):
        return self.city + " - " + self.street


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.address)
