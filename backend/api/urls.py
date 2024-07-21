from django.urls import path
from api.views import Index
from . import views

urlpatterns = [
    path('', Index.as_view(), name='studio'),
    #path('<pk>/', CsvDetails.as_view()),
    path('upload/<int:upload_id>/', views.upload_detail, name='upload_detail'),
    path('analyze/<int:upload_id>/', views.analyze_file, name='analyze-file'),
    path('message/', views.messaging, name='send-message'),
]
