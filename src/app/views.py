from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from allauth.account.views import LoginView
from .context import context
from .forms import UserProfileForm
from django.conf import settings


def netics_home(request):

    return render(request, "mainPage/index.html", context)


def myNetwork(request):
    return render(request, "myNetwork/index.html", context)


def login(request):
    return render(request, "login/index.html", context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        context["form"] = UserProfileForm()

        return render(request, "profilePage/index.html", context)


def login_view(request):
    context = {
        'client_id': settings.CLIENT_ID,
    }
    return render(request, 'login/index.html', context)
