from django.urls import path
from api.views import Index
from . import views

urlpatterns = [
    path('', Index.as_view(), name='studio'),
    #path('<pk>/', CsvDetails.as_view()),
    path('upload/<int:upload_id>/', views.upload_detail, name='upload_detail'),
    path('analyze/<int:upload_id>/', views.analyze_file, name='analyze-file'),
    path('message/', views.messaging, name='send-message'),

    #Path for the dynamic update of column data
    path('update_col_data/<int:upload_id>/', views.update_col_data, name='update_col_data'),
]
