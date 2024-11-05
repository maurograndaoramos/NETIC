from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from allauth.account.views import LoginView
from .context import context
from .forms import UserProfileForm


def netics_home (request) :

    return render (request, "mainPage/index.html", context)

def myNetwork (request): 
    return render (request, "myNetwork/index.html", context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        context["form"] = UserProfileForm()
    
        return render (request, "profilePage/index.html", context)

class CustomLoginView(LoginView):
    template_name = 'account/login.html' 
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)