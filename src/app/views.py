from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from allauth.account.views import LoginView
from .context import context as contextPlaceholder
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth import login, authenticate

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.conf import settings

@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        logged_user_id = data.get('userId')
        user_to_add_id = data.get('userToAdd')

        logged_user_model = UserProfile.objects.get(id=logged_user_id)
        user_to_add_model = UserProfile.objects.get(id=user_to_add_id)

        new_user_to_add_is_on_network = logged_user_model.network.filter(id=user_to_add_model.id).exists()

        if not new_user_to_add_is_on_network:
            logged_user_model.network.add(user_to_add_model)
    

def netics_home (request):
    user_placeholder = authenticate(request, username = "coopercynthia", password = "123456")
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
            "users_data" : UserProfile.objects.all(),
            "logged_user_id" : request.user.id
        }
        login(request, user_placeholder)
        
    return render (request, "mainPage/index.html", context)

def myNetwork (request): 
    logged_profile = UserProfile.objects.get(id=request.user.id)
    all_connected_users = logged_profile.network.all()

    context = {
        "users_data" :all_connected_users,
        "logged_user_id" : request.user.id
    }
    return render (request, "myNetwork/index.html", context)



def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        "form": form,
    }
    return render(request, "profilePage/index.html", context)

def login_view(request):
    context = {
        'client_id': settings.CLIENT_ID,
    }
    return render(request, 'login/index.html', context)

