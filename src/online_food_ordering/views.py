from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.

def homepage(request):
    return render(request, 'online_food_ordering/home.html')


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
