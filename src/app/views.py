from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import UserProfileForm
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from allauth.account.views import LoginView
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import json

@csrf_exempt
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
            
        return JsonResponse({"status": "success"})

def netics_home(request):
    if request.user.is_authenticated:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )

        context = {
            "courses": [
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
            "users_data": UserProfile.objects.all(),
            "logged_user_id": request.user.id
        }

        return render(request, "mainPage/index.html", context)
    else:
        return redirect('login')

def myNetwork(request): 
    if request.user.is_authenticated:
        logged_profile = UserProfile.objects.get(user=request.user)
        all_connected_users = logged_profile.network.all()

        context = {
            "users_data": all_connected_users,
            "logged_user_id": request.user.id
        }
        return render(request, "myNetwork/index.html", context)
    else:
        return redirect('login')

def profile(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('login')

def login_view(request):
    context = {
        'client_id': settings.CLIENT_ID,
    }
    return render(request, 'login/index.html', context)
