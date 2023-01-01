from django.urls import path
from .views import SendInvitationView 

urlpatterns = [
    path('send/', SendInvitationView.as_view()),
]
