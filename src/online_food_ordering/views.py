from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import *


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


class Cart(DetailView):
    model = Order
    template_name = 'online_food_ordering/cart.html'

    def get_queryset(self):
        print(self.request)
        return Order.objects.filter(user_address__user=self.request.user)
