from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.netics_home, name='home'),
    path("network/", views.myNetwork, name = 'network'),
    path("perfil/", views.profile, name='perfil'),
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls'))
]
