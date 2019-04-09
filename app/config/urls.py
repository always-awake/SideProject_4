from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls', namespace='cars')),
    path('api-token-auth/', obtain_jwt_token),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
