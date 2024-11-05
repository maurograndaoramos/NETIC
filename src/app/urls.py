from django.urls import path
from . import views

urlpatterns = [
    path("", views.netics_home, name='home'),
    path("network/", views.myNetwork, name = 'network'),
    path("perfil/", views.profile, name='perfil')
]
