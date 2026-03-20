from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),   # kyunki app ka naam "app" hai
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
