from django.contrib import admin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import SiteAdmin, RestaurantManager, Customer, Address
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'role', 'device', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'role',)}),
    )
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Customer)
class CustomerProxyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', ]
    list_display_links = ['id']
    list_editable = ['email']
    search_fields = ['username', 'email']

    def get_queryset(self, request):
        return Customer.objects.filter(is_staff=False)


@admin.register(RestaurantManager)
class RestaurantManagerProxyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', ]
    list_display_links = ['id']
    list_editable = ['email']
    search_fields = ['username', 'email']

    def get_queryset(self, request):
        return RestaurantManager.objects.filter(is_staff=True, is_superuser=False)


@admin.register(SiteAdmin)
class SiteAdminProxyAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    list_display_links = ['username']
    list_editable = ['email']
    search_fields = ['username', 'email']

    def get_queryset(self, request):
        return SiteAdmin.objects.filter(is_superuser=True)


admin.site.register(Address)
