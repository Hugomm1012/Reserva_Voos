from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from voos.views import pagina_nao_encontrada

handler404 = pagina_nao_encontrada

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voos.urls')),
]

# Servir ficheiros static em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)