from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'curso', 'sinopse', 'instagram', 'github', 'linkedin', 'website', 'descricao_longa', 'profile_picture']
        widgets = {
            'sinopse': forms.Textarea(attrs={'rows': 3}),
            'descricao_longa': forms.Textarea(attrs={'rows': 5}),
            'profile_picture': forms.FileInput(),
        }