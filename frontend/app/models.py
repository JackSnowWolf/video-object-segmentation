from django.db import models

# Create your models here.
class Video(models.Model):
    videoname = models.CharField(max_length = 30)
    File = models.FileField(upload_to= './upload/')

    def __str__(self):
        return self.videoname
