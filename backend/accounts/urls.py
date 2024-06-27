from django.urls import path
from accounts import views
from accounts.views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('', views.accounts_home, name='accounts'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('signin', UserLoginView.as_view(), name='login'),
]
