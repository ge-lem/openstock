from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet

router = DefaultRouter()
router.register(r'orgas', OrganizationViewSet,basename="orga")

urlpatterns = [
    path('', include(router.urls)),
]
