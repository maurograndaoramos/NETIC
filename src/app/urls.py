from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.netics_home, name='home'),
    path("network/", views.myNetwork, name='network'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:chat_id>', views.chat, name='chat'),
    path("perfil/", views.profile, name='perfil'),
    path("receive_id/", views.add_to_network, name='data'),
    path("add_message/", views.add_message, name='add_message'),
    path("get_messages/", views.get_messages, name='add_message'),
    path("get_db_id/", views.return_chat_id, name='get_id'),
    path("remove_id/", views.remove_to_network, name="remove"),
    path('login/', views.login_view, name='login'),
]
