from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .forms import UploadForm
from .models import UploadModel
import csv

# Create your views here.
class Index(TemplateView):
    template_name = 'pages/home/index-test.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = UploadForm() 
        uploads = UploadModel.objects.all()
        
        # Extract file names from the instances
        files = [upload.table_name for upload in uploads]

        context = {'form': form, 'files':files}  # Add form to context
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):  
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the form data
            table_name = form.cleaned_data['table_name']
            uploaded_file = request.FILES['data_file_upload']
            file_name = uploaded_file.name

            if file_name.lower().endswith('.csv'):
                form.save()
            else:
                raise ValueError("Not Good")

            #form.save()

            if form.save():
                success_text = "Saved"

            context = {
                'form':form,
                'success':True,
                'table_name':table_name,
                'succ':success_text,
            }

            return render(request, self.template_name, context)  # Indicate success
        else:
            
            return render(request, self.template_name, {'form': form})  # Redisplay form with errors



class CsvDetails(DetailView):
    template_name = 'pages/home/index-test.html'
    model = UploadModel
