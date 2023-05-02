from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('clients/', include('clients.urls')),
]
