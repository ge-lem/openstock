from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, SearchPostViewSet, ImportPostsViewSet

router = routers.DefaultRouter()
router.register(r'posts/search', SearchPostViewSet, "searchpost")
router.register(r'posts/import', ImportPostsViewSet, "import")
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
