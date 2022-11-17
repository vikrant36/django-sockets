from django.db import models

# Create your models here.


class Answer(models.Model):
    """"""
    candidate_id = models.IntegerField()
    candidate_name = models.CharField(max_length=60)
    question_id = models.IntegerField()
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=1000)

