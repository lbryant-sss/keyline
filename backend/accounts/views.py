from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
        
        print("Form active after POST")
        if form.is_valid():
            print("Form active")
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