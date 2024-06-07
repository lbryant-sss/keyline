from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload', 'table_name']
        widgets = {
            'table_name': forms.TextInput(attrs={
                'class':'form-control',
                'id': 'id_table_name',
                
            }),
            'file_upload': forms.FileInput(attrs={
                'class': 'form-control-file',
                'id': 'file-upload-input',
            })
        }
