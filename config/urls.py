from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", include("catalog.urls", namespace="catalog")
    ),  # urly в корне, без префикса /home/
    path("blog/", include("blog.urls", namespace="blog")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
