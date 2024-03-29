from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),
    path("users/", include("users.urls")),
    path("clients/", include("clients.urls")),
    path("cars/", include("cars.urls")),
    path("prices/", include("prices.urls")),
    path("contracts/", include("contracts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
