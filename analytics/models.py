from django.db import models
from django.utils import timezone
from django.conf import settings

class SearchTerm(models.Model):
    term = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.term} (em {self.timestamp.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        verbose_name = "Termo Buscado"
        verbose_name_plural = "Termos Buscados"
        ordering = ['-timestamp']

class PageView(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    path = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_str = f" (User: {self.user.username})" if self.user else ""
        return f"{self.path} - Session: {self.session_key[:8]}...{user_str} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Visualização de Página"
        verbose_name_plural = "Visualizações de Página"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['session_key', 'timestamp']),
        ]