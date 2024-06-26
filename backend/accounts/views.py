from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from accounts.forms import(
    UserRegistrationForm, UserLoginForm, CustomSetPasswordForm,
)
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

#Password reset view
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

# Create your views here.


def accounts_home(request):
    return render(request, 'pages/auth/home-test.html')


class UserRegistrationView(View):
    template_name = 'pages/auth/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    password = ''
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')

            if(password1 == password2):
                password = password2

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            return redirect('accounts')
     
        else:
            form = UserRegistrationForm()
        
        return render(request, self.template_name, {'form': form})
    

class UserLoginView(View):
    template_name = 'pages/auth/login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        #if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            return redirect('accounts')
                
        else:
            form = UserLoginForm()

        return render(request, self.template_name, {'form': form})
    

def logout_user(request):
    logout(request)
    return redirect('accounts')


class UserPasswordResetView(PasswordResetView):
    template_name = 'pages/auth/reset-password.html'
    email_template_name = 'pages/auth/password_reset_email.html'

    success_url = reverse_lazy('password-reset-done')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pages/auth/reset-password-done.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    #template_name = 'pages/auth/password_reset_confirm.html'
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pages/auth/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password-reset-complete')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    



class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'pages/auth/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
