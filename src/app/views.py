import logging
import logging
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from pydantic import BaseModel, Field, field_validator
from pydantic import BaseModel, Field, field_validator
from .forms import UserProfileForm
from django.http import JsonResponse
from django.http import JsonResponse
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from allauth.account.views import LoginView
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import json
from main.utils.mongoDb import *
from allauth.account.adapter import DefaultAccountAdapter

logging.basicConfig(level=logging.INFO)


# Desativa temporariamente a verificação CSRF (apenas para testes)
@csrf_exempt
def add_to_network(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        logged_user_id = data.get('userId')
        user_to_add_id = data.get('userToAdd')

        logged_user_model = UserProfile.objects.get(id=logged_user_id)
        user_to_add_model = UserProfile.objects.get(id=user_to_add_id)

        new_user_to_add_is_on_network = logged_user_model.network.filter(
            id=user_to_add_model.id).exists()

        if not new_user_to_add_is_on_network:
            logged_user_model.network.add(user_to_add_model)


# Desativa temporariamente a verificação CSRF (apenas para testes)
@csrf_exempt
def remove_to_network(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        logged_user_id = data.get('userId')
        user_to_remove_id = data.get('userToRemove')

        # Retrieve the logged-in user and the user to be removed
        logged_user_model = UserProfile.objects.get(id=logged_user_id)
        user_to_remove_model = UserProfile.objects.get(id=user_to_remove_id)

        # Check if the user is currently in the network
        if logged_user_model.network.filter(id=user_to_remove_model.id).exists():
            # Remove the user from the network
            logged_user_model.network.remove(user_to_remove_model)


class Message(BaseModel):
    user_id: int
    content: str
    sent_time: str


class Chat(BaseModel):
    id: int = Field(alias="_id")
    users: list[int]
    messages: list[Message]

    @field_validator("id", mode="before")
    @classmethod
    def transform(cls, raw: ObjectId) -> int:
        logging.info("raw", raw.__id)

        return int(raw)


# Desativa temporariamente a verificação CSRF (apenas para testes)
@csrf_exempt
def return_chat_id(request):
    data = json.loads(request.body)

    user_id = data.get('user_id')
    user_contact_id = data.get('contact_id')

    print(user_id, user_contact_id)

    mongo_db = mongo_remote_db()
    chat = mongo_db.get_or_create_chat(
        user_id=user_id, friend_id=user_contact_id)

    logging.warning(Chat(**chat))

    return JsonResponse({
        'id': str(chat.get("_id"))
    })

    return JsonResponse({'ui': chat_return.model_dump()})

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

        logged_profile = UserProfile.objects.get(user=request.user)

        excluded_users = logged_profile.network.all()
        users_not_in_network = UserProfile.objects.exclude(
            id__in=excluded_users).exclude(id=logged_profile.id)

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
            # Users not in the network of the logged user
            "users_data": users_not_in_network,
            "logged_user_id": request.user.id,
            "particles": min(len(logged_profile.network.all()) + 2, 100)
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
            "logged_user_id": request.user.id,
            "particles": min(len(logged_profile.network.all()) + 2, 100)
        }
        return render(request, "myNetwork/index.html", context)
    else:
        return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)

        if request.method == 'POST':
            form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
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


Mongo = mongo_remote_db()


def chat(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Retrieve chats associated with the logged-in user
        chats_list = Mongo.get_chats(user_profile.user.id)
        active_users = {}

        for chat in chats_list:
            user_ids = chat['users']  # List of user IDs in the chat

            # Exclude the logged-in user's ID
            other_users = [uid for uid in user_ids if str(
                uid) != str(user_profile.user.id)]

            for user_id in other_users:
                # Retrieve user information for the other users
                user = UserProfile.objects.filter(user_id=user_id).first()
                if user:
                    # Add user information to the active_users dictionary
                    if user_id not in active_users:
                        active_users[user_id] = f"{
                            user.first_name} {user.last_name}"

        # Context passed to the template
        context = {
            'users_list': active_users,  # Dictionary of user_id -> full_name
            'chats_list': chats_list,   # Chats data from MongoDB
            'user_profile': user_profile.user.id  # Logged-in user's ID
        }

        return render(request, 'chat/index.html', context)
    else:
        return redirect('login')


#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['form'] = MessageForm()
#       return context
