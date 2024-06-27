from django.urls import path
from accounts import views
from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetComplete,
    UserPasswordResetConfirmView,
)

urlpatterns = [
    path('', views.accounts_home, name='accounts'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('signin/', UserLoginView.as_view(), name='login'),
    path('signout/', views.logout_user, name='logout'),

    #Password Reset URLS
    path('reset-password', UserPasswordResetView.as_view(), name='password-reset'),
    path('reset-password-done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset-password/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset-password-complete', UserPasswordResetComplete.as_view(), name='password-reset-complete'),
]
