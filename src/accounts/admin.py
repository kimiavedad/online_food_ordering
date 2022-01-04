from django.contrib import admin
from .models import SiteAdmin, RestaurantManager, Customer, Address
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomChangeForm, CustomCreationForm

CustomUser = get_user_model()


class AddressInline(admin.TabularInline):
    model = Customer.addresses.through


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'device',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'role',)}),
    )
    list_display = ['email', 'username', 'date_joined', 'role']
    date_hierarchy = 'date_joined'


@admin.register(Customer)
class CustomerProxyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'device', 'role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
    list_display = ['id', 'username', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['role', 'is_active', 'is_staff', 'is_superuser']
    inlines = [AddressInline, ]

    def get_queryset(self, request):
        return CustomUser.objects.filter(role=CustomUser.Role.CUSTOMER)

    def save_model(self, request, obj, form, change):
        # for hashing password
        obj.set_password(form.cleaned_data["password"])
        obj.save()


@admin.register(RestaurantManager)
class RestaurantManagerProxyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'device', 'role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
    list_display = ['id', 'username', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['role', 'is_active', 'is_staff', 'is_superuser']
    empty_value_display = '-'

    def get_queryset(self, request):
        return CustomUser.objects.filter(role=CustomUser.Role.RESTAURANT_MANAGER)

    def save_model(self, request, obj, form, change):
        # for hashing password
        obj.set_password(form.cleaned_data["password"])
        obj.save()


@admin.register(SiteAdmin)
class SiteAdminProxyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email', 'first_name', 'last_name', 'device', 'role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )
    list_display = ['id', 'username', 'role', 'email', ]
    list_display_links = ['id']
    list_editable = ['username']
    search_fields = ['username', 'email']
    readonly_fields = ['role', 'is_active', 'is_staff', 'is_superuser']

    def get_queryset(self, request):
        return CustomUser.objects.filter(role=CustomUser.Role.SITE_ADMIN)

    def save_model(self, request, obj, form, change):
        # for hashing password
        obj.set_password(form.cleaned_data["password"])
        obj.save()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_filter = ['city']
    list_display = ['id', 'city']
