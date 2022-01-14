from collections import defaultdict
from django.views.generic import TemplateView, ListView, View
from online_food_ordering.models import Order, MenuItem, Restaurant
from accounts.models import Customer, Address
from django.urls import reverse_lazy
from django.http import JsonResponse
from allauth.account.views import SignupView
from .forms import CustomerSignupForm
import re


class CustomerSignUpView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomerSignupForm
    success_url = reverse_lazy('account_login')


class CustomerPanel(TemplateView):
    template_name = "customer/customer_panel.html"


class OrderListView(ListView):
    model = Order
    template_name = "customer/orders.html"

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer=self.request.user, status__gt=0)
        return self.queryset


class CustomerUpdate(TemplateView):
    template_name = "customer/customer_edit.html"

    def post(self, request):
        """
            format of data wh received form frontend is:
            { address[1].city: 'تهران', address[1].street: ' آزادی', address[1].plaque: '134' , primary:1}
            so we want to create a nested dictionary that looks like this:
            {'1': {'city': 'تهران', 'street': 'آزادی', 'plaque': '134'}
        """
        address = defaultdict(dict)
        request_items = list(request.POST.items())[1:-1].copy()

        for k, v in request_items:
            _, no, key = re.split(r'\[(?P<no>\d+)\]\.', k, maxsplit=2)
            address[no][key] = v

        request.user.addresses.all().delete()
        for key, value in address.items():
            Address.objects.create(customer=request.user, city=value['city'], street=value['street'],
                                   plaque=int(value['plaque']))

        primary_address = request.user.addresses.all()[int(request.POST.get("primary")) - 1]
        primary_address.primary = True
        primary_address.save()

        return JsonResponse({'message': 'تغییرات با موفقیت ذخیره شد!'})


def search(request):
    if request.method == "POST" and request.is_ajax():
        searched_content = request.POST.get('searched_content')
        queryset = MenuItem.objects.filter(food__name__contains=searched_content)
        if queryset:
            return JsonResponse({
                "type": "food",
                "object_list":
                    list(queryset.values('pk', 'food__name', 'branch__name', 'branch__restaurant__name', 'price'))
            })

        queryset = Restaurant.objects.filter(name__contains=searched_content)
        if queryset:
            object_list = []
            for res in queryset:
                object_list += list(res.branches.values('pk', 'name', 'restaurant__name', 'primary'))
            return JsonResponse({
                "type": "restaurant",
                "object_list": object_list
            })
        else:
            return JsonResponse({'message': 'نتیجه ای پیدا نشد:('})
    return JsonResponse({})

# class Checkout(View):
#     pass
# todo: 1.get address
# todo: 2.get cart cookie
# todo: 2.delete cart cookie
# todo: 3.create order and order items from this cart
