from rest_framework.routers import DefaultRouter
from django.urls import path
from auth import views


router = DefaultRouter()

router.register(
    prefix='',
    viewset=views.AuthViewSet,
    basename='auth'
)

urlpatterns = router.urls
