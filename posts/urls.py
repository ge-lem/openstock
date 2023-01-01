from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, SearchPostViewSet

router = routers.DefaultRouter()
router.register(r'posts/search', SearchPostViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
