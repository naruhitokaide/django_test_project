
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from feeds import views

urlpatterns = [
    path('', include('feeds.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
