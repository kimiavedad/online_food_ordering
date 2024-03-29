"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from restaurant_manager.views import RestaurantManagerSignUpView
from customer.views import CustomerSignUpView

urlpatterns = [
    path('signup_manager/', RestaurantManagerSignUpView.as_view(), name='signup_manager'),
    path('signup_customer/', CustomerSignUpView.as_view(), name='signup_customer'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('online_food_ordering.urls')),
    path('site_admin/', include('site_admin.urls')),
    path('restaurant_manager/', include('restaurant_manager.urls')),
    path('customer/', include('customer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
