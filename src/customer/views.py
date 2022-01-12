from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from online_food_ordering.models import Order


class CustomerPanel(TemplateView):
    template_name = "customer/customer_panel.html"


class OrderListView(ListView):
    model = Order
    template_name = "customer/orders.html"

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer=self.request.user, status__gt=0)
        print(self.queryset)
        return self.queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(OrderListView, self).get_context_data()
    #     context['branch'] = .items.first()

# class Checkout(View):
#     pass
# todo: 1.get address
# todo: 2.get cart cookie
# todo: 2.delete cart cookie
# todo: 3.create order and order items from this cart
