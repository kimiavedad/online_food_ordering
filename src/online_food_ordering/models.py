from django.db import models

import jdatetime


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

    @property
    def date_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at)


class Branch(models.Model):
    manager = models.OneToOneField('accounts.RestaurantManager', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='branches')
    address = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    primary = models.BooleanField()

    class Meta:
        verbose_name_plural = 'branches'

    def __str__(self):
        return self.restaurant.name + " " + self.name

    @property
    def date_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at)


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
    customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, )

    def __str__(self):
        return "order" + str(self.id)

    @property
    def date_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at)

    @property
    def total_price(self):
        order_items = self.items.all()
        total_price = sum([item.total for item in order_items])
        return total_price

    @property
    def number_of_items(self):
        order_items = self.items.all()
        number_of_items = sum([item.quantity for item in order_items])
        return number_of_items


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return str(self.menu_item) + " - " + str(self.order) + "-" + str(self.price)

    @property
    def total(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.menu_item.price
        return super().save(*args, **kwargs)

    def is_same_restaurant(self, branch):
        return self.menu_item.branch == branch
