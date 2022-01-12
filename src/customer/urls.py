from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomerPanel.as_view(), name='customer_panel'),
    path('orders/', OrderListView.as_view(), name='orders'),
]
