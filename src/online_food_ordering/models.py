from django.db import models
from django.urls import reverse


class Restaurant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    meals = models.ManyToManyField(Meal)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='food_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    manager = models.OneToOneField('accounts.RestaurantManager', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='branches')
    address = models.OneToOneField('accounts.Address', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    primary = models.BooleanField()

    class Meta:
        verbose_name_plural = 'branches'

    def __str__(self):
        return self.restaurant.name + " " + self.name


class MenuItem(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='menu')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='menu')
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.branch) + " - " + self.food.name


class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'سفارش'),
        (1, 'ثبت'),
        (2, 'ارسال'),
        (3, 'تحویل'),
    ]
    user_address = models.ForeignKey('accounts.UserAddress', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES,)

    def __str__(self):
        return "order" + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return str(self.menu_item) + " - " + str(self.order)
