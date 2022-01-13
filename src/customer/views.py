from collections import defaultdict

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from online_food_ordering.models import Order
from accounts.models import Customer, Address
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.forms import inlineformset_factory
import re


class CustomerPanel(TemplateView):
    template_name = "customer/customer_panel.html"


class OrderListView(ListView):
    model = Order
    template_name = "customer/orders.html"

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer=self.request.user, status__gt=0)
        print(self.queryset)
        return self.queryset


class CustomerUpdate(TemplateView):
    template_name = "customer/customer_edit.html"

    def post(self, request):
        print()
        address = defaultdict(dict)
        request_items = list(request.POST.items())[1:].copy()
        for k, v in request_items:
            _, no, key = re.split(r'\[(?P<no>\d+)\]\.', k, maxsplit=2)
            address[no][key] = v

        request.user.addresses.all().delete()
        for key, value in address.items():
            print(value)
            Address.objects.create(customer=request.user, city=value['city'], street=value['street'],
                                   plaque=int(value['plaque']))

        print(request.user.addresses.all())
        return JsonResponse({'message': 'تغییرات با موفقیت ذخیره شد!'})

# def update_customer(request):
#     # AddressInlineFormSet = inlineformset_factory(Customer, Address, exclude=('customer',), extra=1)
#     customer = request.user
#     if request.method == 'POST':
#         print('yes')
#         # formset = AddressInlineFormSet(request.POST, instance=customer)
#         # print(formset.is_valid())
#         # print(formset)
#         # if formset.is_valid():
#         #     objects = formset.save()
#         #     print(objects)
#         # Do something. Should generally end with a redirect. For example:
#
#         return redirect('customer_panel')
#         # return HttpResponseRedirect('customer_panel')
#
#         # formset = AddressInlineFormSet(instance=customer)
#     return render(request, "customer/customer_edit.html", {'address_list': customer.addresses.all()})


# class Checkout(View):
#     pass
# todo: 1.get address
# todo: 2.get cart cookie
# todo: 2.delete cart cookie
# todo: 3.create order and order items from this cart
