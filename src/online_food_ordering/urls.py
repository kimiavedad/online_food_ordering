from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path(r'login_success/$', login_success, name='login_success' )
]
