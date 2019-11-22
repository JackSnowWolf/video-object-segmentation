from django.db import models

# Create your models here.
class Video(models.Model):
    videoname = models.CharField(max_length = 30)
    Frame = models.FileField(upload_to='./upload/First_Frame')
    File = models.FileField(upload_to= './upload/File')

    def __str__(self):
        return self.videoname
