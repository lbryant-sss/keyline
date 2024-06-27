from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm

class UserRegistrationForm(forms.ModelForm):
    #Custom fields for password confirmation
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email', 'username',
        ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        # Example: Custom validation for new_password2
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match")

        return new_password2
    