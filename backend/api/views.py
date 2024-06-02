from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import UploadForm

# Create your views here.
class Index(TemplateView):
    template_name = 'pages/home/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = UploadForm()  # Initialize the form
        context = {'form': form}  # Add form to context
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):  
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the form data
            table_name = form.cleaned_data['table_name']
            file_upload = form.cleaned_data['file_upload']
            
            form.save()

            context = {
                'form':form,
                'success':True,
                'table_name':table_name,
            }

            return render(request, self.template_name, context)  # Indicate success
        else:
            return render(request, self.template_name, {'form': form})  # Redisplay form with errors
