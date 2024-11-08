from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.conf import settings
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True)
    curso = models.CharField(max_length=50, blank=True)
    sinopse = models.TextField(max_length=150, blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    descricao_longa = models.TextField(blank=True)
    network = models.ManyToManyField('self', blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['curso', 'first_name']

    def __str__(self):
        return f'{self.user.username} - {self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return f'/perfil/{self.id}/'

    def get_network(self):
        return self.network.all()

@receiver(user_logged_in)
def create_profile_on_login(sender, request, user, **kwargs):
    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
    )