from django.contrib.auth.models import User
from django.db import models
from main.settings import MEDIA_ROOT

# Create your models here.
class UserProfile (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=50)
    sinopse = models.TextField(max_length=150, blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to = MEDIA_ROOT)
    descricao_longa = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    network = models.ManyToManyField('self', blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['curso', 'first_name']

    def __str__(self):
        return self.id
    
    def get_absolute_url(self):
        return f'/perfil/{self.id}/'
    
    def get_network(self):
        return self.network.all()