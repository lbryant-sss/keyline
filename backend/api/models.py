from django.db import models


#Upload Model
class UploadModel(models.Model):
    default_name = 'Default Table Name'
    table_name = models.CharField(max_length=100, default=default_name)
    created_at = models.DateTimeField(auto_now_add=True)
    data_file_upload = models.FileField(upload_to='uploads/tables/')

    def __str__(self):
        return self.table_name

class MessagingModel(models.Model):
    sender_username = models.CharField(max_length=100)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


