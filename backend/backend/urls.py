from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
