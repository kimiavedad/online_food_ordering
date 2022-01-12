from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('login_success/', login_success, name='login_success'),

    path('restaurant/<int:pk>/', BranchDetailView.as_view(), name='branch_detail'),
    path('restaurant/all/', BranchListView.as_view(), name='branch_list'),

    path('cart/', cart, name="cart"),
    path('update_order/', update_order, name="update_order"),

    path('food/<int:pk>', FoodDetailView.as_view(), name='food_detail'),

    path('customer_panel/', CustomerPanel.as_view(), name='admin_panel'),


]
