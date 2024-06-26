from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(forms.ModelForm):
    #Custom fields for password confirmation
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email', 'username',
        ]
