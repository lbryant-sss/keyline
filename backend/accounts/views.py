from django.shortcuts import render

# Create your views here.


def accounts_home(request):
    return render(request, 'pages/auth/home-test.html')


class UserRegistrationView():
    pass