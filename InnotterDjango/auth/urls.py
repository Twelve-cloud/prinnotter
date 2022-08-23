from rest_framework.routers import DefaultRouter
from django.urls import path
from auth import views


router = DefaultRouter()

router.register(
    prefix='auth',
    viewset=views.AuthViewSet,
)

urlpatterns = router.urls
