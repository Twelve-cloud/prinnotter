from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('login/', views.LoginAPIView.as_view(), name='login')
]
