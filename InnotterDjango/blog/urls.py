from rest_framework_extensions.routers import ExtendedDefaultRouter
from django.urls import path
from blog import views


router = ExtendedDefaultRouter()
(
    router.register(prefix='pages',
                    viewset=views.PageViewSet,
                    basename='pages')
          .register(prefix='posts',
                    viewset=views.PostViewSet,
                    basename='pages-posts',
                    parents_query_lookups=['page_id'])
)

router.register(prefix='tags', viewset=views.TagViewSet, basename='tags')

urlpatterns = router.urls

urlpatterns += [
    path('search/', views.search),
    path('news/', views.news),
]
