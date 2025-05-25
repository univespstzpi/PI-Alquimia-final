from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models
from analytics.models import SearchTerm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProdutoSerializer

# Create your views here.
class Lista(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']

class Detalhe(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class ProdutoSearchView(APIView):
    def get(self, request, format=None):
        termo_busca = request.query_params.get('termo').strip()    
        if termo_busca:
            SearchTerm.objects.create(
                term=termo_busca.lower(),
                user=request.user if request.user.is_authenticated else None
            )

            produtos = models.Produto.objects.filter(nome__icontains=termo_busca)
            return render(request, 'produto/lista.html', {'produtos': produtos})
            # serializer = ProdutoSerializer(produtos, many=True)
            # return Response(serializer.data)
        else:
            return Response({'error': 'Termo de busca não fornecido'}, status=status.HTTP_400_BAD_REQUEST)