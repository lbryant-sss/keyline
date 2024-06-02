from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload', 'table_name']
