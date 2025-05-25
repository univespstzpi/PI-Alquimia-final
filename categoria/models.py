from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    @staticmethod
    def get_all_categorias():
        return Categoria.objects.all()

    def __str__(self):
        return self.nome
