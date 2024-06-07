from django.urls import path
from api.views import Index
from . import views

urlpatterns = [
    path('', Index.as_view(), name='index-test'),
    #path('<pk>/', CsvDetails.as_view()),
    path('upload/<int:upload_id>/', views.upload_detail, name='upload_detail'),
]
