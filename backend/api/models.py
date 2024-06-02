from django.db import models


#Upload Model
class UploadModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    data_file_upload = models.FileField(upload_to='uploads/')

