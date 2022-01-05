from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
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
    except Exception:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(user_address__user=customer, status=0)
    print(order.__dict__)
    return render(request, 'online_food_ordering/cart.html', {'order': order})
