from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SendInvitationView, InvitationViewSet

router = DefaultRouter()
router.register(r'invitations', InvitationViewSet,basename="invitations")

urlpatterns = [
    path('', include(router.urls)),
    path('invitations/send/', SendInvitationView.as_view()),
]
