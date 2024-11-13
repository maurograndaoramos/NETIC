from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.netics_home, name='home'),
    path("network/", views.myNetwork, name='network'),
    path('chat/', views.chat, name='chat'),
    path("perfil/", views.profile, name='perfil'),
    path("receive_id/", views.add_to_network, name='data'),
    path("remove_id/", views.remove_to_network, name="remove"),
    path('login/', views.login_view, name='login'),
]
