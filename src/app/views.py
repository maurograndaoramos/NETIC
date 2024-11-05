from django.shortcuts import redirect, render
from .context import context as contextPlaceholder
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth import login, authenticate

def netics_home (request) :
    user_placeholder = authenticate(request, username = "Admin", password = "Password")
    if user_placeholder is not None :
        context = {
            "courses" : [
                "Design de Comunicação e Marketing Digital",
                "Criação Musical, Produção e Técnicas de Som",
                "Design de Comunicação e Multimédia",
                "Fotografia Profissional",
                "Programação Web",
                "Realização, Cinema e TV",
                "Videojogos",
                "Concept Art",
                "Design Gráfico",
                "Fotografia",
                "Marketing Digital e Social Media",
                "Produção e Criação Musical Eletrónica",
                "Técnicas de Som"
            ],
            "users_data" : UserProfile.objects.all()
        }
        login(request, user_placeholder)
        
        return render (request, "mainPage/index.html", context)

def myNetwork (request): 
    return render (request, "myNetwork/index.html", contextPlaceholder)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        context["form"] = UserProfileForm()
    
        return render (request, "profilePage/index.html", concontextPlaceholdertext)