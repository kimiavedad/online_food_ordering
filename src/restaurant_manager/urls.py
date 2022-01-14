from django.urls import path
from .views import *

urlpatterns = [
    path('', RestaurantManagerPanel.as_view(), name='restaurant_manager_panel'),   
    path('orders/', OrderListView.as_view(), name='orders'),
    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('menu/<int:pk>/delete/', MenuItemDelete.as_view(), name='menuitem_delete'),
    path('menu/<int:pk>/', MenuItemUpdate.as_view(), name='menuitem_edit'),
    path('menu/new/', MenuItemCreateView.as_view(), name='menuitem_create'),
]
