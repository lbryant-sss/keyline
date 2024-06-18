from django import forms
from .models import UploadModel, MessagingModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload', 'table_name']
        widgets = {
            'table_name': forms.TextInput(attrs={
                'class':'form-control',
                'id': 'id_table_name',
                'required': True,
            }),
            'file_upload': forms.FileInput(attrs={
                'class': 'default-file-input',
                'id': 'file-upload-input',
                'required': True,
            })
        }

class MessagingForm(forms.ModelForm):
    class Meta:
        model = MessagingModel

        fields = [
            'sender_username',
            'sender_email',
            'subject',
            'body',
        ]
    