from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload']

    def clean_file_upload(self):
        file = self.cleaned_data.get('file_upload')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("Only .csv files are allowed.")
        return file
