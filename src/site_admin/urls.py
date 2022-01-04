from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminPanel.as_view(), name='admin_panel'),

    path('food/all/', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>/edit/', FoodUpdateView.as_view(), name='food_edit'),
    path('food/<int:pk>/delete/', FoodDeleteView.as_view(), name='food_delete'),
    path('food/new/', FoodCreateView.as_view(), name='food_new'),

    path('category/new/', CategoryCreateView.as_view(), name='category_new'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', CategoryListView.as_view(), name='category_list'),
]
