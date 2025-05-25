from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.Carrinho.as_view(), name='carrinho'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name="adicionaraocarrinho"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name="removerdocarrinho"),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name="resumodacompra"),
]

