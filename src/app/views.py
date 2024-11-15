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

# class Message(BaseModel):
#     user_id: int
#     content: str
#     sent_time: str

# class Chat(BaseModel):
#     id: int = Field(alias="_id")
#     users: list[int]
#     messages: list[Message]



#     @field_validator("id", mode="before")
#     @classmethod
#     def transform(cls, raw: ObjectId) -> int:
#         logging.info("raw", raw.__id)

#         return int(raw)


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


@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def get_messages(request) :
    data = json.loads(request.body)

    chat_id = data.get('chat_id')    
    mongo_db = mongo_remote_db()
    all_messages = mongo_db.get_messages(
        chat_id=chat_id
    )

    return JsonResponse ({
        'message' : all_messages
    })

@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def get_chats(request) :
    data = json.loads(request.body)

    chat_id = data.get('chat_id')    
    mongo_db = mongo_remote_db()
    all_messages = mongo_db.get_messages(
        chat_id=chat_id
    )

    return JsonResponse ({
        'message' : all_messages
    })

@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def add_message(request) :
    data = json.loads(request.body)

    user_id = data.get('user_id')
    chat_id = data.get('chat_id')
    content_message = data.get('content_message')
    
    mongo_db = mongo_remote_db()
    mongo_db.add_message(
        chat_id=chat_id,
        user_id= user_id,
        msg_content=content_message
    )

    return JsonResponse ({
        'message' : f'{user_id} {chat_id} {content_message}'
    })

@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def get_user_chats(request) :
    data = json.loads(request.body)

    user_id = data.get('user_id')

    mongo_db = mongo_remote_db()
    chats = mongo_db.get_chats(user_id=user_id)

    formated_chats = []
    for chat in chats:
        chat_id = chat.get("_id")
        friend_name = ""
        friend_id = 0

        friend_user = ""
        friend_user_profile=""

        for user_chat_id in chat["users"] :
            if str(user_chat_id) != str(request.user.id):
                friend_id = user_chat_id
                
                friend_user = User.objects.all().filter(id=friend_id)[0]
                friend_user_profile = UserProfile.objects.all().filter(user = friend_user)[0]

                friend_name = f'{friend_user_profile.first_name} {friend_user_profile.last_name}'
                
        messages = mongo_db.get_messages(chat_id=chat_id)
        if messages :
            last_message = messages[len(messages)-1]['content']
        else :
            last_message = ""

        formated_chats.append(
            {
                "id": str(chat_id),
                "friend_id" : friend_id,
                "friend_name" : str(friend_name),
                "last_message" : last_message
            }
        )
    
    return JsonResponse ({
        'chats' : formated_chats
    })

@csrf_exempt  # Desativa temporariamente a verificação CSRF (apenas para testes)
def get_user_info(request) :
    data = json.loads(request.body)

    user_id = data.get('user_id')
    auth_user = User.objects.all().filter(id = user_id)[0]

    user_contact_profile = UserProfile.objects.all().filter(user=auth_user)
    
    user_contact_profile_info = {
        "id" : user_contact_profile[0].id,
        "first_name" : user_contact_profile[0].first_name,
        "last_name" : user_contact_profile[0].last_name,
        "course" : user_contact_profile[0].curso,
        # "profile_picture" : user_contact_profile[0].profile_picture.url,
    }

    return JsonResponse ({
        'user_info' : user_contact_profile_info
    })

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

def chat(request, chat_id):

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        logged_profile = UserProfile.objects.get(user=request.user)

        # Retrieve chats associated with the logged-in user
        chats_list = Mongo.get_chats(user_profile.user.id)
        active_users = {}

        this_chat_users = Mongo.get_or_create_chat(chat_id=chat_id).get("users")

        contact_id = ""

        for chat_user_id in this_chat_users :
            if str(chat_user_id) != str(request.user.id) :
                contact_id += chat_user_id

        context= {
            'chats_list': chats_list,
            'all_chats': all_chats,
            'user_profile': user_profile.user.id,
            "chat_id" : chat_id,
            "user_id": request.user.id,
            "contact_id" : contact_id,
            "particles" : min(len(logged_profile.network.all()) + 2, 100) 

        }

        return render(request, 'chat/index.html', context)
    else:
        return redirect('login')

    
def chats(request):
    if request.user.is_authenticated:
        logged_profile = UserProfile.objects.get(user=request.user)

        context= {
            "user_id": request.user.id,
            "particles" : min(len(logged_profile.network.all()) + 2, 100) 

        }

        return render(request, 'chat/chat.html', context)
    else:
        return redirect('login')

