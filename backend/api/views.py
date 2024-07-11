from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from .forms import UploadForm, MessagingForm
from .models import UploadModel, MessagingModel
import csv
from django.http import HttpResponse
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings



class Index(TemplateView):
    template_name = 'pages/home/studio.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        uploads = UploadModel.objects.all()
        
        files = [{'id': upload.id, 'name': upload.table_name} for upload in uploads]

        selected_upload_id = request.GET.get('upload_id')
        selected_column = request.GET.get('selected_column')  # Add this to get selected column
        selected_upload = None
        data = None
        table_name = ''
        file_path = ''
        analysis_results = None
        csv_data_shape = ()
        data_type_info = {}
        rows_with_missing_values = 0
        column_names = []
        csv_data = ''
        

        if selected_upload_id:
            try:
                selected_upload = UploadModel.objects.get(id=selected_upload_id)
                table_name = selected_upload.table_name
                data = self.process_uploaded_file(selected_upload.data_file_upload)
                file_path = selected_upload.data_file_upload.path

                # Load CSV data into a Pandas DataFrame
                csv_data = pd.read_csv(file_path)

                 # Calculate statistics for each numeric column individually
                
                # Calculate statistics for each numeric column
             
               # Count rows with any missing values
                rows_with_missing_values = len(csv_data[csv_data.isnull().any(axis=1)])

                # Get column names from the DataFrame
                column_names = csv_data.columns.tolist()

            except UploadModel.DoesNotExist:
                print(f"UploadModel with ID {selected_upload_id} does not exist")

        data_rows = csv_data.shape[0]
        data_columns = csv_data.shape[1]

        context = {
            'form': form,
            'files': files,
            'data': data,
            'selected_upload_id': selected_upload_id,
            'table_name': table_name,
            'file_path': file_path,
            'csv_data_shape': csv_data_shape,
            'data_rows': data_rows,
            'data_columns': data_columns,
            'data_types': data_type_info,
            'rows_with_missing_values': rows_with_missing_values,
            'column_names': column_names,
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

            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {'form': form})

    def process_uploaded_file(self, uploaded_file):
        decoded_file = uploaded_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        data = list(reader)
        return data
        
 


def upload_detail(request, upload_id):
    return render(request, 'pages/upload_detail.html', {'upload_id': upload_id})


def analyze_file(request, upload_id):
    #csv_file = UploadModel.objects.get(id=upload_id)
    #file_path = csv_file.file.path
    csv_file = get_object_or_404(UploadModel, id=upload_id)
    file_path = csv_file.data_file_upload.path
    
    if file_path:
        print("File Path is: ", file_path)

    else:
        print("File Path not found")

    return render(request, 'pages/analyze.html', {'path': file_path})


def messaging(request):
    if request.method == 'POST':
        form = MessagingForm(request.POST)
        if form.is_valid():
            sender_username = form.cleaned_data['sender_username']
            sender_email = form.cleaned_data['sender_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # Compose the message body to include the sender's username and the actual message body
            message_body = f"Sender: {sender_username}, {sender_email}\n\n{body}"

            # Send email
            send_mail(
                subject,
                message_body,  # Include both sender's username and the actual message body
                sender_email,
                [settings.DEFAULT_FROM_EMAIL],  # This should be the recipient list
                fail_silently=False,
            )

            message_sent = "Message sent!"

            return HttpResponse("Message Sent!")
        else:
            return HttpResponse("Message Not sent!")
    else:
        form = MessagingForm()

    return render(request, 'pages/home/messaging.html', {'form': form})