from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'curso', 'email', 'synopsis', 'instagram', 'github', 'linkedin', 'otherlink', 'long_description']
        widgets = {
            'synopsis': forms.Textarea(attrs={'rows': 3}),
            'long_description': forms.Textarea(attrs={'rows': 5}),
        }