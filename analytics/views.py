from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from .models import SearchTerm

# @staff_member_required # Garante que apenas membros da equipe (admin) possam acessar
# def top_searched_terms_report(request):
#     # Define o número de termos principais a serem exibidos
#     limit = request.GET.get('limit', 20)
#     try:
#         limit = int(limit)
#     except ValueError:
#         limit = 20

#     top_terms = SearchTerm.objects.values('term') \
#         .annotate(search_count=Count('term')) \
#         .order_by('-search_count')[:limit]

#     context = {
#         'top_terms': top_terms,
#         'title': 'Relatório de Termos Mais Buscados'
#     }
#     return render(request, 'admin/analytics/top_searched_terms_report.html', context)