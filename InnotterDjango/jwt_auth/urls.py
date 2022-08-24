from rest_framework.routers import DefaultRouter
from django.urls import path
from jwt_auth import views


router = DefaultRouter()

router.register(
<<<<<<< HEAD:InnotterDjango/auth/urls.py
    prefix='',
    viewset=views.AuthViewSet,
    basename='auth'
=======
    prefix='jwt',
    viewset=views.AuthViewSet,
    basename='jwt',
>>>>>>> 344f632 (fix: some fixes):InnotterDjango/jwt_auth/urls.py
)

urlpatterns = router.urls
