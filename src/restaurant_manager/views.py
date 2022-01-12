from django.shortcuts import render
from online_food_ordering.models import Order
from django.views.generic import ListView, TemplateView


class RestaurantManagerPanel(TemplateView):
    template_name = "restaurant_manager/restaurant_manager_panel.html"


class OrderListView(ListView):
    model = Order
    template_name = "restaurant_manager/orders.html"

    def get_queryset(self):
        return Order.objects.exclude(status=0).filter(items__menu_item__branch=self.request.user.branch)

    def post(self, request):
        pass
