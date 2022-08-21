from rest_framework.routers import DefaultRouter
from django.urls import path
from user import views


router = DefaultRouter()

router.register(
    prefix='users',
    viewset=views.UserViewSet
)

urlpatterns = router.urls

urlpatterns += [
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('refresh/', views.RefreshTokenApiView.as_view(), name='refresh'),
    path('login/', views.LoginAPIView.as_view(), name='login')
]
