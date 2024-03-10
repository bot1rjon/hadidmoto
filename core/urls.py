from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('akhmadjonov_komron/', admin.site.urls),

    path('', include('web.urls')),
    path('sklad/', include('control.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "web.views.page404"