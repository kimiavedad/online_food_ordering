from django.shortcuts import render
from online_food_ordering.models import Order, MenuItem, Food
from django.views.generic import ListView, TemplateView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse


class RestaurantManagerPanel(TemplateView):
    template_name = "restaurant_manager/restaurant_manager_panel.html"


class OrderListView(ListView):
    model = Order
    template_name = "restaurant_manager/orders.html"

    def get_queryset(self):
        return Order.objects.filter(status__gt=0).filter(items__menu_item__branch=self.request.user.branch).distinct()

    def post(self, request):
        status = {'ارسال': 2, 'تحویل': 3}
        if request.is_ajax():
            order_index = int(request.POST.get('order_index'))
            order = self.get_queryset()[order_index]
            order.status = status.get(request.POST.get('status'))
            order.save()
            return JsonResponse({})


class MenuItemListView(ListView):
    model = MenuItem
    template_name = "restaurant_manager/menu.html"

    def get_queryset(self):
        return MenuItem.objects.filter(branch=self.request.user.branch)


class MenuItemDelete(DeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu')


class MenuItemUpdate(UpdateView):
    model = MenuItem
    template_name = 'restaurant_manager/menuitem_edit.html'
    fields = ['stock', 'price']
    success_url = reverse_lazy('menu')


class MenuItemCreateView(CreateView):
    model = MenuItem
    template_name = 'restaurant_manager/menuitem_create.html'
    fields = ['food', 'stock', 'price']
    success_url = reverse_lazy('menu')

    def get_form_class(self):
        form_class = super().get_form_class()
        branch = self.request.user.branch
        foods_in_menu = branch.menu.values_list('food', flat=True).distinct()
        form_class.base_fields.get('food').queryset = Food.objects.exclude(pk__in=foods_in_menu).filter(
            category=branch.category)
        return form_class

    def form_valid(self, form):
        form.instance.branch = self.request.user.branch
        return super(MenuItemCreateView, self).form_valid(form)
