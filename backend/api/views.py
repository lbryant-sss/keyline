from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import UploadForm
from .models import UploadModel
import csv
from .analysis import calculate_statistics
import pandas as pd
import matplotlib.pyplot as plt
from django.utils._os import safe_join


class Index(TemplateView):
    template_name = 'pages/home/index.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        uploads = UploadModel.objects.all()
        
        # Extracting file names and ids from the instances
        files = [{'id': upload.id, 'name': upload.table_name} for upload in uploads]

        # Check if a specific upload was selected
        selected_upload_id = request.GET.get('upload_id')
        analyze_upload_id = request.GET.get('analyze_id')
        selected_upload = None
        data = None
        table_name = ''
        file_path = ''
        analysis_results = None


        if selected_upload_id:
            try:
                selected_upload = UploadModel.objects.get(id=selected_upload_id)
                table_name = selected_upload.table_name
                # Process the selected upload's file for display
                data = self.process_uploaded_file(selected_upload.data_file_upload)

                ##Processing the csv data
                #Gets the file path
                file_path = selected_upload.data_file_upload.path

                ##Convert to df
                csv_data = pd.read_csv(file_path)

                csv_data_shape = csv_data.shape
                #data_type_info = csv_data.dtypes.to_dict()
                data_type_info = {column: str(csv_data[column].dtype) for column in csv_data.columns}

                ##DRAWING A GRAPH FROM CSV DATA
                            # Plot bar chart
                columns = list(data_type_info.keys())
                data_type_counts = [list(data_type_info.values()).count('int64'),
                                    list(data_type_info.values()).count('float64'),
                                    list(data_type_info.values()).count('object')]
                plt.bar(columns, data_type_counts)
                plt.xlabel('Data Types')
                plt.ylabel('Count')
                plt.title('Data Types Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig('media/graphs/data_type_info.png')  # Save the plot as a PNG file
                plt.close()



            except UploadModel.DoesNotExist:
                print(f"UploadModel with ID {selected_upload_id} does not exist")

        context = {
            'form': form,
            'files': files,
            'data': data,
            'selected_upload_id': selected_upload_id,
            'table_name': table_name,
            'file_path': file_path,
            # Added for template consistency
            #pandas analysis results
            'csv_data_shape': csv_data_shape,
            'data_types': data_type_info,
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

