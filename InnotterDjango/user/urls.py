from rest_framework.routers import DefaultRouter
from django.urls import path
from user import views


router = DefaultRouter()

router.register(
    prefix='users',
    viewset=views.UserViewSet,
    basename='users',
)

urlpatterns = router.urls
