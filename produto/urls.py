from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.Lista.as_view(), name='lista'),
    path('buscar/', views.ProdutoSearchView.as_view(), name='buscar'),
    path('<slug>', views.Detalhe.as_view(), name="detalhe"),
]