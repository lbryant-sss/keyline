from django.urls import path
from api.views import Index, CsvDetails

urlpatterns = [
    path('', Index.as_view(), name='index-test'),
    #path('<pk>/', CsvDetails.as_view()),
]
