from django import forms
from .models import UploadModel

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['data_file_upload', 'table_name']

    def clean_data_file_upload(self):  # Renamed to match the field name
        file = self.cleaned_data.get('data_file_upload')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("Only .csv files are allowed.")
        return file
