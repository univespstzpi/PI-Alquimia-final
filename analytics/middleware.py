from django.utils import timezone
from .models import PageView
from django.conf import settings

# Caminhos a serem excluídos do registro de visualização de página
EXCLUDED_PATHS_PREFIXES = [
    '/admin/',
    '/static/',
    '/media/',
    '/api/'
]
if hasattr(settings, 'ANALYTICS_EXCLUDED_PATHS_PREFIXES'):
    EXCLUDED_PATHS_PREFIXES.extend(settings.ANALYTICS_EXCLUDED_PATHS_PREFIXES)

class PageViewLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Garante que a sessão seja criada e tenha uma chave
        if not request.session.session_key:
            request.session.create()

        response = self.get_response(request)

        # Verifica se o caminho deve ser excluído
        if any(request.path.startswith(prefix) for prefix in EXCLUDED_PATHS_PREFIXES):
            return response

        # Registra visualizações de página para requisições GET bem-sucedidas que parecem ser HTML
        # Você pode querer refinar isso (ex: verificar Content-Type)
        if request.method == 'GET' and response.status_code == 200:
            user = request.user if request.user.is_authenticated else None
            PageView.objects.create(
                session_key=request.session.session_key,
                user=user,
                path=request.path,
                timestamp=timezone.now() 
            )
        return response