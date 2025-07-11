from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')),
    path('principal/', include('django.contrib.auth.urls')),
    path('principal/', include('principal.urls')),

    
]
