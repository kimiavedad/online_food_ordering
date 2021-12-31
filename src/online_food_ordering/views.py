from django.shortcuts import render


# Create your views here.

def homepage(request):
    return render(request, 'online_food_ordering/home.html')


def admin_panel(request):
    return render(request, 'online_food_ordering/admin_panel.html')
