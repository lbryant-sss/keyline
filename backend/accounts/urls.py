from django.urls import path
from accounts import views
from accounts.views import UserRegistrationView

urlpatterns = [
    path('', views.accounts_home, name='accounts'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
