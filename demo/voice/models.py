from django.db import models

# Create your models here.


class Voice(models.Model):
    """"""
    audio = models.FileField(upload_to='audio_file')
