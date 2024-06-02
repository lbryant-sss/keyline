from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import UploadForm

# Create your views here.
class Index(TemplateView):
    template_name = 'pages/home/index.html'

    def get(self, request, *args, **kwargs):
        context  = {}
        return render(request, self.template_name, context)


def my_form_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the form data
            created_at = form.cleaned_data['created_at']
            file_upload = form.cleaned_data['file_upload']
            
            # Here you can save the data to the database or process it
            # ...
            form.save()

            return render(request, 'success.html', {'form': form})
    else:
        form = UploadForm()

    return render(request, 'form_template.html', {'form': form})
