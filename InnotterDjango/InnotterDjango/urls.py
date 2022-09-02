from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/auth/', include('jwt_auth.urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/blog/', include('blog.urls')),
]
