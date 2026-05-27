from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mail_management_service/", include("mail_management_service.urls", namespace="mail_management_service")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
