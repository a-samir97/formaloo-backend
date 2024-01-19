from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Formaloo Backend Task API",
      default_version='v1',
      description="Backend Task API"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Django Dashboard
    path("admin/", admin.site.urls),
    # Apps URLs
    path("api/", include('appstore.urls')),
    path("api/", include('users.urls')),
    # Swagger
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
