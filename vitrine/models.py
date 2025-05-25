from django.db import models

# Create your models here.
class Vitrine(models.Model):
    nome = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    status = models.BooleanField()