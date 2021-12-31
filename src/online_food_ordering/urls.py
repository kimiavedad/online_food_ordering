from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('admin_panel/', admin_panel, name='admin_panel')
]