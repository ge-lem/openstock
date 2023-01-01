from django.urls import path, include

from djoser import views as djsoer_views
from knox import views as knox_views

from rest_framework.routers import DefaultRouter
from myauth.views import LoginView, UserList

router = DefaultRouter()
router.register('users', djsoer_views.UserViewSet)

djoser_urlpatterns = [
    path(r'users/search/', UserList.as_view()),
    path(r'', include(router.urls)),   ### If you want to add user view set
]

knox_urlpatterns = [
    path(r'login/', LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

urlpatterns = knox_urlpatterns + djoser_urlpatterns
