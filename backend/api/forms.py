from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload', 'table_name']
        widgets = {
            'table_name': forms.TextInput(attrs={
                'class':'form-control',
                'id': 'table_name_input',
                
            }),
            'file_upload': forms.FileInput(attrs={
                'class': 'form-control-file',
                'id': 'file-upload-input',
            })
        }
