from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
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

    if request.user.is_authenticated:
        customer = request.user
    else:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order = None
    if Order.objects.filter(customer=customer, status=0).exists():
        order = Order.objects.get(customer=customer, status=0)
    return render(request, 'online_food_ordering/cart.html', {'order': order})


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
        print(order_item)

        order = Order.objects.get(customer=customer, status=0)
        print(order.items.all()[int(order_item)])
        order.items.all()[int(order_item)].delete()
        if not order.items.all():
            order.delete()
        return JsonResponse({})
    return JsonResponse({})
