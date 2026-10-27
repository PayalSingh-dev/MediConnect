"""
URL configuration for Healthcare Backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def health_check(request):
    return JsonResponse(
        {
            'status': 'healthy',
            'service': 'Healthcare Backend API',
            'documentation': '/api/docs/',
            'ui': '/',
        }
    )


urlpatterns = [
    # Interactive Healthcare Portal UI
    path('', TemplateView.as_view(template_name='index.html'), name='portal-ui'),

    # Admin
    path('admin/', admin.site.urls),

    # Health check JSON
    path('health/', health_check, name='health'),

    # OpenAPI 3 Schema & Interactive Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Application APIs
    path('api/auth/', include('apps.authentication.urls')),
    path('api/patients/', include('apps.patients.urls')),
    path('api/doctors/', include('apps.doctors.urls')),
    path('api/mappings/', include('apps.mappings.urls')),
]
