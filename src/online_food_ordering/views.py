from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse

from .models import *
from accounts.models import Customer


def homepage(request):
    top_food_list = Food.objects.filter(menu__orders__order__status__gt=0).distinct().annotate(
        total=Sum('menu__orders__quantity')).order_by('-total')[:10]
    top_restaurant_list = Branch.objects.filter(menu__orders__order__status__gt=0).distinct().annotate(
        total=Sum('menu__orders__quantity')).order_by('-total')[:10]

    return render(request, 'online_food_ordering/home.html',
                  context={'top_food_list': top_food_list, 'top_restaurant_list': top_restaurant_list})


def login_success(request):
    """
    Redirects users based on who they are
    """
    if request.user.role == 'ادمین سایت':
        # user is an admin
        return redirect("admin_panel")
    elif request.user.role == 'مدیر رستوران':
        # return redirect("other_view")
        return
    else:
        return redirect('home')


class BranchDetailView(ListView):
    model = MenuItem
    template_name = "online_food_ordering/branch_detail.html"

    def get_queryset(self):
        return MenuItem.objects.filter(branch=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['branch'] = Branch.objects.get(pk=self.kwargs['pk'])
        return context


def cart(request):
    try:
        customer = request.user
        # user_address = UserAddress.objects.
    except Exception:
        print(request.COOKIES['device'])
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    # order, created = Order.objects.get_or_create(customer=customer, status=0)
    print(order.__dict__)
    return render(request, 'online_food_ordering/cart.html', {'order': order})


class FoodDetailView(DetailView):
    model = MenuItem
    template_name = "online_food_ordering/food_detail.html"

    def post(self, request, *args, **kwargs):
        menu_item = MenuItem.objects.get(pk=self.kwargs['pk'])
        try:
            customer = request.user
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        print(customer)
        order, created = Order.objects.get_or_create(user_address__user=customer, status=0)
        order_item, created = OrderItem.objects.get_or_create(order=order, menu_item=menu_item)
        order_item.quantity = request.POST['quantity']
        order_item.save()
        return redirect('cart')

# def update_order(request):
#     if request.method == "POST" and request.is_ajax():
#         try:
#             customer = request.user.customer
#         except:
#             device = request.COOKIES['device']
#             customer, created = Customer.objects.get_or_create(device=device)
#
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#         orderItem.quantity = request.POST['quantity']
#         orderItem.save()
#         return JsonResponse({})
#     return JsonResponse({})
