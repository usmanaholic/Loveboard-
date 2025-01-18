from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('messages_wall.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),  # For authentication
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
