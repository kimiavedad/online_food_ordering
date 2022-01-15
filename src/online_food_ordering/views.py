from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.contrib import messages
from .models import *
from accounts.models import Customer


def homepage(request):
    top_food_list = Food.objects.filter(menu__orders__order__status__gt=0).distinct().annotate(
        total=Sum('menu__orders__quantity')).order_by('-total')[:10]
    top_restaurant_list = Branch.objects.filter(menu__orders__order__status__gt=0).distinct().annotate(
        total=Sum('menu__orders__quantity')).order_by('-total')[:10]

    return render(request, 'online_food_ordering/home.html',
                  context={'top_food_list': top_food_list, 'top_restaurant_list': top_restaurant_list})


class BranchListView(ListView):
    model = Branch
    template_name = "online_food_ordering/branch_list.html"


def login_success(request):
    """
    Redirects users based on who they are
    """
    if request.user.role == 'ادمین سایت':
        # user is an admin
        return redirect("admin_panel")
    elif request.user.role == 'مدیر رستوران':
        return redirect("restaurant_manager_panel")
    else:
        return redirect("customer_panel")


class BranchDetailView(ListView):
    model = MenuItem
    template_name = "online_food_ordering/branch_detail.html"

    def get_queryset(self):
        return MenuItem.objects.filter(branch=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['branch'] = Branch.objects.get(pk=self.kwargs['pk'])
        return context


class FoodDetailView(DetailView):
    model = MenuItem
    template_name = "online_food_ordering/food_detail.html"

    def post(self, request, *args, **kwargs):
        menu_item = self.get_object()
        if request.user.is_authenticated:
            customer = request.user
        else:
            device = request.COOKIES['device']
            customer, bool_created = Customer.objects.get_or_create(device=device, username=device)

        if int(request.POST.get('quantity')) > menu_item.stock:
            messages.error(request, "تعداد انتخابی بیشتر از موجودی رستوران است.")
            return redirect(reverse('branch_detail', kwargs={'pk': menu_item.branch.pk}))

        if Order.objects.filter(customer=customer, status=0).exists():
            order = Order.objects.get(customer=customer, status=0)
            if not order.items.first().is_same_restaurant(menu_item.branch):
                order.items.all().delete()
                messages.info(request, "سبد خرید قبلی شما پاک شد!")

        else:
            order = Order.objects.create(customer=customer, status=0)
        order_item, bool_created = OrderItem.objects.get_or_create(order=order, menu_item=menu_item)
        order_item.quantity = request.POST['quantity']
        order_item.save()
        messages.success(request, f"{menu_item.food.name} به سبد خرید اضافه شد.")
        return redirect(reverse('branch_detail', kwargs={'pk': menu_item.branch.pk}))


def update_order(request):
    if request.method == "POST" and request.is_ajax():
        if request.user.is_authenticated:
            customer = request.user
        else:
            device = request.COOKIES['device']
            customer, bool_created = Customer.objects.get_or_create(device=device)

        order_item = request.POST.get('order_item')

        order = Order.objects.get(customer=customer, status=0)
        order.items.all()[int(order_item)].delete()
        if not order.items.all():
            order.delete()
        return JsonResponse({})
    return JsonResponse({})


def get_cart(customer):
    if Order.objects.filter(customer=customer, status=0).exists():
        return Order.objects.filter(customer=customer, status=0).first()
    return None


def set_cart_for_real_customer(request, order):
    real_customer = request.user
    real_customer_order, created = Order.objects.get_or_create(customer=real_customer, status=0)
    real_customer_order.items.all().delete()
    real_customer_order.items.set(list(order.items.all()))
    order.delete()
    return real_customer_order


class CartView(View):
    def get(self, request, *args, **kwargs):
        device = self.request.COOKIES.get('device')
        if Customer.objects.filter(device=device).exists() and self.request.user.is_authenticated:
            device_customer = Customer.objects.filter(device=device).last()
            device_cart = get_cart(device_customer)
            if device_cart:
                order = set_cart_for_real_customer(self.request, device_cart)
                device_customer.delete()
            else:
                order = get_cart(self.request.user)
        else:
            if request.user.is_authenticated:
                customer = request.user
            else:
                customer, created = Customer.objects.get_or_create(username=device, device=device)
            order = get_cart(customer)
        return render(request, 'online_food_ordering/cart.html', {'order': order})

    def post(self, request):
        queryset = self.request.user.addresses.all()
        return JsonResponse({"addresses": list(queryset.values('city', 'street', 'plaque', 'primary'))})

