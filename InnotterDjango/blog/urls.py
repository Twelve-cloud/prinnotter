from rest_framework_extensions.routers import ExtendedDefaultRouter
from blog import views


router = ExtendedDefaultRouter()

router.register(
    prefix='tags',
    viewset=views.TagViewSet,
    basename='tags'
)

router.register(
    prefix='pages',
    viewset=views.PageViewSet,
    basename='pages'
).register(
    prefix='posts',
    viewset=views.PostViewSet,
    basename='pages-posts',
    parents_query_lookups=['page_id']
)

urlpatterns = router.urls
