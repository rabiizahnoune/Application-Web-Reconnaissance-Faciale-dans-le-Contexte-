from django.db import models
from django.contrib.auth.models import User


# models.py



class RecognitionResult(models.Model):
    label = models.CharField(max_length=100)
    image = models.ImageField(upload_to='facial_recognition_results/')
    similarity_score = models.FloatField()
    

    # Ajoutez d'autres champs selon vos besoins



