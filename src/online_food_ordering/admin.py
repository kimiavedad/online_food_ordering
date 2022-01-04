from .models import *
from django.contrib import admin

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(MenuItem)
admin.site.register(OrderItem)


class MenuItemsInline(admin.TabularInline):
    model = MenuItem


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    inlines = [MenuItemsInline]
    list_per_page = 1


class OrderItemInline(admin.StackedInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    extra = 0
