from django.urls import path
from .views import *

urlpatterns = [
    path('', RestaurantManagerPanel.as_view(), name='restaurant_manager_panel'),   
    path('orders/', OrderListView.as_view(), name='orders'),
]
