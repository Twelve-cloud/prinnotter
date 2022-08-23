from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),
]
