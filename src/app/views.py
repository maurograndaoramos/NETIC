from django.shortcuts import redirect, render
from context import context
from main.forms import ProfileForm
from main.forms import FileForm

def netics_home (request) :

    return render (request, "mainPage/index.html", context)

def myNetwork (request): 
    return render (request, "myNetwork/index.html", {})

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        context["form"] = ProfileForm()
    
        return render (request, "profilePage/index.html", context)