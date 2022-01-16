from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy

from online_food_ordering.models import Food, Category


class AbstractSiteAdmin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.role == "ادمین سایت"


class AdminPanel(AbstractSiteAdmin, TemplateView):
    template_name = 'site_admin/admin_panel.html'


class FoodListView(AbstractSiteAdmin, ListView):
    model = Food
    template_name = 'site_admin/food_list.html'
    fields = '__all__'


class FoodCreateView(AbstractSiteAdmin, CreateView):
    model = Food
    template_name = 'site_admin/food_new.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')


class FoodUpdateView(AbstractSiteAdmin, UpdateView):
    model = Food
    template_name = 'site_admin/food_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')


class FoodDeleteView(AbstractSiteAdmin, DeleteView):
    model = Food
    template_name = 'site_admin/food_delete.html'
    success_url = reverse_lazy('food_list')


class CategoryCreateView(AbstractSiteAdmin, CreateView):
    model = Category
    template_name = 'site_admin/category_new.html'
    fields = '__all__'
    success_url = reverse_lazy('category_list')


class CategoryListView(AbstractSiteAdmin, ListView):
    model = Category
    template_name = 'site_admin/category_list.html'


class CategoryDetailView(AbstractSiteAdmin, ListView):
    model = Food
    template_name = 'site_admin/food_list.html'

    def get_queryset(self):
        return Food.objects.filter(category=self.kwargs['pk'])
