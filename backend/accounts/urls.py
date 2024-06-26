from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.accounts_home, name='accounts'),
]
