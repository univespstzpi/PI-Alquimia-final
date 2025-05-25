from django.db import models

# Create your models here.
class Carrinho(models.Model):
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.UUIDField()
    produto_id = models.PositiveIntegerField()
    qtd_produto = models.PositiveIntegerField()
    preco_unitario = models.FloatField()