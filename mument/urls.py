from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import ProtectedView

schema_view = get_schema_view(
   openapi.Info(
      title="Mument API",
      default_version='v0',
      description="Django REST Framework API for Mument",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/users/', include('users.urls')),
    path('api/report/', include('report.urls')),  
    path('api/coordinators/', include('coordinators.urls')),
    path('api/checkpoint/',include('checkpoint.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
