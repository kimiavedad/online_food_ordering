from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy

from online_food_ordering.models import Food, Category


class AdminPanel(TemplateView):
    template_name = 'site_admin/admin_panel.html'


class FoodListView(ListView):
    model = Food
    template_name = 'site_admin/food_list.html'
    fields = '__all__'


class FoodCreateView(CreateView):
    model = Food
    template_name = 'site_admin/food_new.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')


class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'site_admin/food_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')


class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'site_admin/food_delete.html'
    success_url = reverse_lazy('food_list')


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'site_admin/category_new.html'
    fields = '__all__'
    success_url = reverse_lazy('category_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'site_admin/category_list.html'


class CategoryDetailView(ListView):
    model = Food
    template_name = 'site_admin/food_list.html'

    def get_queryset(self):
        return Food.objects.filter(category=self.kwargs['pk'])
