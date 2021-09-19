from django.contrib import admin
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('chat/', include('messenger.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/users/', include('authentication.urls', namespace='authentication')),
]
