from django.urls import path
from api.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index-test'),
]
