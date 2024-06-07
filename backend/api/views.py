from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import UploadForm
from .models import UploadModel
import csv



class Index(TemplateView):
    template_name = 'pages/home/index.html'
    #'pages/home/index-test.html'
    
    def get(self, request, *args, **kwargs):
        form = UploadForm()
        uploads = UploadModel.objects.all()
        
        # Extract file names and ids from the instances

        files = [
            {'id': upload.id, 'name':upload.table_name} for upload in uploads
        ]

        # Check if a specific upload was selected
        selected_upload_id = request.GET.get('upload_id')
        print("Full GET request parameters:", request.GET)
        print("Selected upload ID: ", selected_upload_id)
        selected_upload = None
        data = None

        if selected_upload_id:
            try:
                selected_upload = UploadModel.objects.get(id=selected_upload_id)
                print("Selected upload:", selected_upload)
                # Process the selected upload's file for display
                data = self.process_uploaded_file(selected_upload.data_file_upload)
                if data is None:
                    print("Processed data is None")
                elif not data:
                    print("Processed data is empty")
                else:
                    print("Processed data:", data)
                
                print("Processed data:", data)
            except UploadModel.DoesNotExist:
                 print(f"UploadModel with ID {selected_upload_id} does not exist")
        context = {
            'form': form,
            'files': files,
            'data': data,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):  
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            table_name = form.cleaned_data['table_name']
            uploaded_file = request.FILES['data_file_upload']
            file_name = uploaded_file.name

            if file_name.lower().endswith('.csv'):
                form.save()
            else:
                raise ValueError("Not a valid CSV file")

            success_text = "Saved successfully" if form.save() else "Save failed"

            context = {
                'form': form,
                'success': True,
                'table_name': table_name,
                'succ': success_text,
            }

            return render(request, self.template_name, context)  # Indicate success
        else:
            return render(request, self.template_name, {'form': form})  # Redisplay form with errors

    def process_uploaded_file(self, uploaded_file):
        # Decode the file if it's in bytes
        decoded_file = uploaded_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        data = list(reader)
        return data
    

def upload_detail(request, upload_id):
    return render(request, 'pages/upload_detail.html', {'upload_id':upload_id})