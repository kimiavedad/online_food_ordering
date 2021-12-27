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
    list_display = ['email', 'username', 'date_joined']
    date_hierarchy = 'date_joined'


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Customer)
class CustomerProxyAdmin(admin.ModelAdmin):
    fields = ['email', 'role']
    list_display = ['id', 'username', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['email', ]

    def get_queryset(self, request):
        return Customer.objects.filter(is_staff=False)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(RestaurantManager)
class RestaurantManagerProxyAdmin(admin.ModelAdmin):
    fields = ['email', 'role']
    list_display = ['id', 'first_name', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['first_name']
    search_fields = ['username', 'email']
    readonly_fields = ['email', ]
    empty_value_display = '-'

    def get_queryset(self, request):
        return RestaurantManager.objects.filter(is_staff=True, is_superuser=False)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SiteAdmin)
class SiteAdminProxyAdmin(admin.ModelAdmin):
    fields = ['email', 'role']
    list_display = ['id', 'username', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['email', ]

    def get_queryset(self, request):
        return SiteAdmin.objects.filter(is_superuser=True)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_filter = ['city']
    list_display = ['id', 'city']

