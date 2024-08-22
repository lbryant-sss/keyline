import json
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from .forms import UploadForm, MessagingForm
from .models import UploadModel, MessagingModel
import csv
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

from django import forms


class Index(TemplateView):
    template_name = 'pages/home/studio.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        uploads = UploadModel.objects.all()
        
        files = [{'id': upload.id, 'name': upload.table_name} for upload in uploads]

        selected_upload_id = request.GET.get('upload_id')
        selected_column_index = request.GET.get('selected_column')
       
        selected_column = ''
        selected_upload = None
        data = None
        table_name = ''
        file_path = ''
        analysis_results = None
        csv_data_shape = ()
        data_type_info = {}
        rows_with_missing_values = 0
        column_names = []
        csv_data = None
        data_rows = 0
        data_columns = 0
        no_csv_data_error_message = ''
        col_data_list = []

        

        if selected_upload_id:
            try:
                #This retrieves the selected file
                selected_upload = UploadModel.objects.get(id=selected_upload_id)
                
                #This accesses the selected table attributes
                table_name = selected_upload.table_name
                data = self.process_uploaded_file(selected_upload.data_file_upload)
                file_path = selected_upload.data_file_upload.path

                # Load CSV data into a Pandas DataFrame
                if file_path is not None:
                    try:
                        csv_data = pd.read_csv(file_path)
                    except Exception as e:
                        no_csv_data_error_message = f"Error loading CSV file: {e}"
                else:
                    no_csv_data_error_message = "File path is None."
                

                if csv_data is not None:
                    data_rows = csv_data.shape[0]
                    data_columns = csv_data.shape[1]
                    
                    
                else:
                    no_csv_data_error_message = "Failed to load csv information."

                 # Calculate statistics for each numeric column individually
                
                # Calculate statistics for each numeric column
             
               # Count rows with any missing values
                rows_with_missing_values = len(csv_data[csv_data.isnull().any(axis=1)])

                # Get column names from the DataFrame
                column_names = csv_data.columns.tolist()


                #This is to get the selected row for analysis and graph
                default_col_name = column_names[1]
                selected_column = request.GET.get('selected_column', default_col_name)
                #default selected column data
                col_data = csv_data[selected_column]
                col_data_list = col_data.tolist()
                

            except UploadModel.DoesNotExist:
                pass
                #print(f"UploadModel with ID {selected_upload_id} does not exist")

            

        #data_rows = csv_data.shape[0]
        #data_columns = csv_data.shape[1]

        context = {
            'form': form,
            'files': files,
            'data': data,
            'selected_upload_id': selected_upload_id,
            'table_name': table_name,
            'file_path': file_path,
            'csv_data_shape': csv_data_shape,
            #'data_rows': data_rows,
            #'data_columns': data_columns,
            'data_types': data_type_info,
            'rows_with_missing_values': rows_with_missing_values,
            'column_names': column_names,
            #Selected column from dropdown
            'selected_column': selected_column,
            #selected column data
            "col_data_list": col_data_list,

            'data_rows': data_rows,
            'data_columns': data_columns,
            'no_csv_data_error_message': no_csv_data_error_message,
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
    
def update_col_data(request, upload_id):
    selected_upload_id = upload_id
    uploads = UploadModel.objects.all()
    files = [{'id': upload.id, 'name': upload.table_name} for upload in uploads]
    selected_upload = UploadModel.objects.get(id=selected_upload_id)

    upload_instance = get_object_or_404(UploadModel, id=selected_upload_id)


    file_path = selected_upload.data_file_upload.path
    context = {}
    csv_data = pd.read_csv(file_path)
    # Get column names from the DataFrame
    column_names = csv_data.columns.tolist()
    #This is to get the selected row for analysis and graph
    default_col_name = column_names[1]
    selected_column = request.GET.get('selected_column', default_col_name)
    #default selected column data
    col_data = csv_data[selected_column]
    col_data_list = col_data.tolist()
    
    context = {
        "col_data_list": col_data_list,
    }
    
    return render(request, 'pages/partials/col_update.html', context)
        


def upload_detail(request, upload_id):
    selected_upload_id = upload_id
    uploads = UploadModel.objects.all()
    files = [{'id': upload.id, 'name': upload.table_name} for upload in uploads]
    selected_upload = UploadModel.objects.get(id=selected_upload_id)

    upload_instance = get_object_or_404(UploadModel, id=selected_upload_id)

    created_at = upload_instance.created_at
    name = upload_instance.table_name

    file_path = selected_upload.data_file_upload.path
    df = pd.read_csv(file_path)  # Correctly reading the CSV file

    # Handle form submission
    if request.method == 'POST':
        table_data = request.POST.get('tableData')
        table_data = json.loads(table_data)  # Deserialize the table data from JSON

        # Update the DataFrame with the new data
        new_df = pd.DataFrame(table_data, columns=df.columns)
        new_df.to_csv(file_path, index=False)  # Save the updated CSV

        # Redirect to the same page after saving
        return HttpResponseRedirect(request.path_info)

    # If not POST, just display the file data
    field_names = []
    for i in range(len(df)):
        field_row = []
        for column in df.columns:
            field_row.append(f"{column}_{i}")
        field_names.append(field_row)

    data = df.values.tolist()  # Convert DataFrame to a list of lists for rendering in the template

    context = {
        'upload_id': upload_id,
        'file': files,
        'data': data,
        'columns': df.columns,
        'created_at': created_at,
        'name': name,
    }

    return render(request, 'pages/upload_detail.html', context)


def analyze_file(request, upload_id):
    #csv_file = UploadModel.objects.get(id=upload_id)
    #file_path = csv_file.file.path
    csv_file = get_object_or_404(UploadModel, id=upload_id)
    file_path = csv_file.data_file_upload.path
    
    if file_path:
        print("File Path is: ", file_path)

    else:
        print("File Path not found")


    #Processing for repeated and NULL values to style them

    styles = {}

    table_df = pd.read_csv(file_path)

    #NULL values
    for column in table_df.columns:
        for index, value in table_df[column].items():
            x = pd.isnull(value)
            if not x:
                styles[(index, column)] = 'null-value'

    context = {
        'path': file_path,
        'styles': styles,
    }

    return render(request, 'pages/analyze.html', context=context)


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