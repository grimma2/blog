from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from userposts import urls as userposts_urls
from userinteractive import urls as userinteractive_urls
from myblog import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('userposts/', include(userposts_urls)),
    path('userinteractive/', include(userinteractive_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
