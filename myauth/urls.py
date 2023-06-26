from django.urls import path, include
from django.conf import settings

from djoser import views as djsoer_views
from knox import views as knox_views

from rest_framework.routers import DefaultRouter

from myauth.views import LoginView, UserList, SelfView

router = DefaultRouter()
router.register('users', djsoer_views.UserViewSet)

users_urlpatterns = [
    path(r'users/search/', UserList.as_view()),
]

djoser_urlpatterns = [
    path(r'', include(router.urls)),
]

knox_urlpatterns = [
    path(
        r'login/',
        LoginView.as_view(),
        name='knox_login'),
    path(
        r'logout/',
        knox_views.LogoutView.as_view(),
        name='knox_logout'),
    path(
        r'logoutall/',
        knox_views.LogoutAllView.as_view(),
        name='knox_logoutall'),
]

if settings.CAS_AUTH:
    import django_cas_ng.views
    users_urlpatterns.append(
        path(
            'cas/login/',
            django_cas_ng.views.LoginView.as_view(),
            name='cas_ng_login'))
    users_urlpatterns.append(
        path(
            'cas/logout/',
            django_cas_ng.views.LogoutView.as_view(),
            name='cas_ng_logout'))
    users_urlpatterns.append(path('users/me/', SelfView.as_view()))
else:
    users_urlpatterns += djoser_urlpatterns

urlpatterns = knox_urlpatterns + users_urlpatterns
