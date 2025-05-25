from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    fields = ('produto', 'produto_id', 'preco', 'preco_promocional', 'quantidade', 'imagem')
    readonly_fields = ('produto', 'produto_id', 'preco', 'preco_promocional', 'quantidade', 'imagem')
    extra = 0  # Do not show empty forms for adding new items inline
    can_delete = False # Prevent deleting items from an existing order via inline

    def has_add_permission(self, request, obj=None):
        # Prevent adding items directly through admin inline if business logic dictates otherwise
        return False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_link', 'total_formatado', 'qtd_total', 'status', 'get_item_count')
    list_filter = ('status', 'usuario')
    search_fields = ('id', 'usuario__username')
    readonly_fields = ('total', 'qtd_total') # These fields are likely calculated
    inlines = [ItemPedidoInline]
    list_per_page = 20
    ordering = ['-id'] # Show newest orders first

    def usuario_link(self, obj):
        if obj.usuario:
            link = reverse("admin:auth_user_change", args=[obj.usuario.id])
            return format_html('<a href="{}">{}</a>', link, obj.usuario.username)
        return "-"
    usuario_link.short_description = 'Usuário'
    usuario_link.admin_order_field = 'usuario'

    def total_formatado(self, obj):
        return f'R$ {obj.total:_.2f}'.replace('.', ',').replace('_', '.')
    total_formatado.short_description = 'Total'
    total_formatado.admin_order_field = 'total'

    def get_item_count(self, obj):
        return obj.itempedido_set.count()
    get_item_count.short_description = 'Qtd. Itens'

    actions = ['marcar_como_enviado', 'marcar_como_finalizado', 'marcar_como_aprovado']

    def marcar_como_enviado(self, request, queryset):
        updated_count = queryset.update(status='E')
        self.message_user(request, f"{updated_count} pedidos marcados como Enviados.")
    marcar_como_enviado.short_description = "Marcar selecionados como Enviado"

    def marcar_como_finalizado(self, request, queryset):
        updated_count = queryset.update(status='F')
        self.message_user(request, f"{updated_count} pedidos marcados como Finalizados.")
    marcar_como_finalizado.short_description = "Marcar selecionados como Finalizado"

    def marcar_como_aprovado(self, request, queryset):
        updated_count = queryset.update(status='A')
        self.message_user(request, f"{updated_count} pedidos marcados como Aprovados.")
    marcar_como_aprovado.short_description = "Marcar selecionados como Aprovado"


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido_info', 'produto', 'preco_formatado', 'preco_promocional_formatado', 'quantidade')
    list_filter = ('produto', 'pedido__status') # Filter by product or by status of the parent order
    search_fields = ('produto', 'pedido__id', 'pedido__usuario__username')
    list_per_page = 20
    # All fields are read-only as items are typically managed via the order creation process
    readonly_fields = ('pedido', 'produto', 'produto_id', 'preco', 'preco_promocional', 'quantidade', 'imagem')
    ordering = ['-pedido__id', 'id']

    def pedido_info(self, obj):
        link = reverse("admin:pedido_pedido_change", args=[obj.pedido.id])
        return format_html('<a href="{}">Pedido N. {}</a>', link, obj.pedido.pk)
    pedido_info.short_description = 'Pedido'
    pedido_info.admin_order_field = 'pedido'

    def preco_formatado(self, obj):
        return f'R$ {obj.preco:_.2f}'.replace('.', ',').replace('_', '.')
    preco_formatado.short_description = 'Preço Unit.'
    preco_formatado.admin_order_field = 'preco'

    def preco_promocional_formatado(self, obj):
        if obj.preco_promocional > 0:
            return f'R$ {obj.preco_promocional:_.2f}'.replace('.', ',').replace('_', '.')
        return "-"
    preco_promocional_formatado.short_description = 'Preço Promo.'
    preco_promocional_formatado.admin_order_field = 'preco_promocional'

    # Prevent modifications if items are strictly part of an order's lifecycle
    def has_add_permission(self, request):
        return False # Items should be added via the Pedido creation process

    def has_delete_permission(self, request, obj=None):
        return False # Items should not be deleted individually from an order this way