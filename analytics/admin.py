from django.contrib import admin
from django.shortcuts import render
from django.db.models import Count, Min, Max, Sum
from .models import SearchTerm, PageView
from pedido.models import ItemPedido
# from .views import top_searched_terms_report
from django.urls import path
from django.utils import timezone
import json # Adicionar import json

# Registro do SearchTermAdmin com o custom_admin_site
@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'user', 'timestamp_formatted')
    list_filter = ('timestamp', 'user')
    search_fields = ('term', 'user__username')
    readonly_fields = ('term', 'user', 'timestamp')
    date_hierarchy = 'timestamp'
    change_list_template = 'admin/analytics/changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('termos-buscados/', self.admin_site.admin_view(self.top_searched_terms_report), name='analytics_relatorio_termos_buscados'),
            path('taxa-rejeicao/', self.admin_site.admin_view(self.bounce_rate_report_view), name='analytics_bounce_rate_report'),
            path('produtos-mais-vendidos/', self.admin_site.admin_view(self.best_selling_products_report_view), name='analytics_best_selling_products_report'),
        ]
        return custom_urls + urls

    def timestamp_formatted(self, obj):
        return obj.timestamp.strftime("%d/%m/%Y %H:%M:%S")
    timestamp_formatted.admin_order_field = 'timestamp'
    timestamp_formatted.short_description = 'Data/Hora da Busca'

    def has_add_permission(self, request):
        # Termos são adicionados programaticamente pela busca
        return False

    def top_searched_terms_report(self, request):
        # Define o número de termos principais a serem exibidos
        limit = request.GET.get('limit', 20)
        try:
            limit = int(limit)
        except ValueError:
            limit = 20

        top_terms = SearchTerm.objects.values('term') \
            .annotate(search_count=Count('term')) \
            .order_by('-search_count')[:limit]

        base_context = self.admin_site.each_context(request)
        context = {
            **base_context,
            'top_terms': top_terms,
            'title': 'Relatório de Termos Mais Buscados',
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/analytics/top_searched_terms_report.html', context)

    def bounce_rate_report_view(self, request):
        days_filter = request.GET.get('days', '30')
        try:
            days = int(days_filter)
            if days <= 0: days = 30
        except ValueError:
            days = 30
        
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)

        page_views_in_window = PageView.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)

        session_counts = page_views_in_window.values('session_key').annotate(
            page_count=Count('id'),
            first_view_time=Min('timestamp'),
            last_view_time=Max('timestamp')
        ).order_by()

        total_sessions = session_counts.count()
        bounced_sessions_count = 0

        for session in session_counts: # session_counts já é o resultado da agregação
            if session['page_count'] == 1:
                bounced_sessions_count += 1

        bounce_rate = (bounced_sessions_count / total_sessions) * 100 if total_sessions > 0 else 0

        base_context = self.admin_site.each_context(request)
        context = {
            **base_context,
            'title': f'Relatório de Taxa de Rejeição (Últimos {days} dias)',
            'bounce_rate': bounce_rate,
            'total_sessions': total_sessions,
            'bounced_sessions_count': bounced_sessions_count,
            'start_date': start_date,
            'end_date': end_date,
            'days_filter': days,
            'opts': self.model._meta, 
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/analytics/bounce_rate_report.html', context)

    def best_selling_products_report_view(self, request):
        limit_param = request.GET.get('limit', '10')
        try:
            limit = int(limit_param)
            if limit <= 0:
                limit = 10
        except ValueError:
            limit = 10

        valid_sale_statuses = ['A', 'E', 'F']  # Aprovado, Enviado, Finalizado

        # Agrupa por nome do produto e soma as quantidades
        # Idealmente, agruparíamos por produto_id se 'produto' (nome) pudesse ser inconsistente
        # ou se tivéssemos um FK para um modelo Produto.
        # Dada a estrutura atual, agrupar pelo nome 'produto' é o mais direto.
        best_selling = ItemPedido.objects.filter(
            pedido__status__in=valid_sale_statuses
        ).values(
            'produto'  # Nome do produto como string
        ).annotate(
            total_quantity_sold=Sum('quantidade')
        ).order_by('-total_quantity_sold')[:limit]

        product_labels = [item['produto'] for item in best_selling]
        product_data = [item['total_quantity_sold'] for item in best_selling]

        base_context = self.admin_site.each_context(request)
        context = {
            **base_context,
            'title': f'Top {limit} Produtos Mais Vendidos (Status: Aprovado, Enviado, Finalizado)',
            'best_selling_products': best_selling,
            'product_labels_json': json.dumps(product_labels), # Passar como string JSON
            'product_data_json': json.dumps(product_data),     # Passar como string JSON
            'current_limit': limit,
            'opts': self.model._meta, # Usando _meta do SearchTerm, mas poderia ser de um modelo mais genérico se este admin fosse para relatórios gerais
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/analytics/best_selling_products_report.html', context)

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'session_key_short', 'user', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('path', 'session_key', 'user__username')
    readonly_fields = ('session_key', 'user', 'path', 'timestamp')
    date_hierarchy = 'timestamp'
    list_per_page = 30

    def session_key_short(self, obj):
        return obj.session_key[:8] + "..." if obj.session_key else "N/A"
    session_key_short.short_description = "Session Key (curta)"
