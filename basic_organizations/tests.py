from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, RequestsClient, force_authenticate
from .models import Organization
from .views import OrganizationViewSet
from django.contrib.auth import get_user_model
# Create your tests here.

class OrganizationTests(APITestCase):
    def test_organisation_autocreate(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        self.assertIs(Organization.objects.all().count(),1)
        o = Organization.objects.all().first()
        self.assertEqual(o.name,u.username)
        self.assertEqual(o.contact,u.email)
        self.assertIs(o.isIndividual,True)
        self.assertEqual(o.owner,u)

    def test_anonymous(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")

        url = reverse('orga-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_individual_readonly(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'get': 'retrieve'})
        request = factory.get(reverse('orga-detail',args=(u.myorganizations.first().id, 'pk')))
        force_authenticate(request, user=u)
        response = view(request, pk=u.myorganizations.first().id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        view = OrganizationViewSet.as_view(actions={'patch': 'partial_update'})
        data = { 'name' : "change name" }
        request = factory.patch(reverse('orga-detail',args=(u.myorganizations.first().id, 'pk')), data)
        force_authenticate(request, user=u)
        response = view(request, pk=u.myorganizations.first().id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_create(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'post': 'create'})
        data = { 'name' : "SupO", "contact":"e@ex.fr", "owner":u.id }
        request = factory.post(reverse('orga-list'), data)
        force_authenticate(request, user=u)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Organisation name is unique case insensitive
        data = { 'name' : "supO", "contact":"e@ex.fr", "owner":u.id }
        request = factory.post(reverse('orga-list'), data)
        force_authenticate(request, user=u)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0].code, 'unique')

    def test_owner_update_delete(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        o = Organization(name="supO",contact="con@ex.fr",owner=u)
        o.save()

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'patch': 'partial_update'})
        data = { 'name' : "change name" }
        request = factory.patch(reverse('orga-detail',args=(o.id, 'pk')), data)
        force_authenticate(request, user=u)
        response = view(request, pk=o.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(pk=o.id).name, "change name")

        view = OrganizationViewSet.as_view(actions={'delete': 'destroy'})
        request = factory.delete(reverse('orga-detail',args=(o.id, 'pk')))
        force_authenticate(request, user=u)
        response = view(request, pk=o.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_manager_update_nodelete(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        m = User.objects.create_user("manager", "test@example.fr","fakepass")
        o = Organization(name="supO",contact="con@ex.fr",owner=u)
        o.save()
        o.managers.add(m)
        o.save()

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'patch': 'partial_update'})
        data = { 'name' : "change name" }
        request = factory.patch(reverse('orga-detail',args=(o.id, 'pk')), data)
        force_authenticate(request, user=m)
        response = view(request, pk=o.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(pk=o.id).name, "change name")

        view = OrganizationViewSet.as_view(actions={'delete': 'destroy'})
        request = factory.delete(reverse('orga-detail',args=(o.id, 'pk')))
        force_authenticate(request, user=m)
        response = view(request, pk=o.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authuser_get(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        o = Organization(name="supO",contact="con@ex.fr",owner=u)
        o.save()

        au = User.objects.create_user("authuser", "test@example.fr","fakepass")

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'get': 'retrieve'})
        request = factory.get(reverse('orga-detail',args=(o.id, 'pk')))
        force_authenticate(request, user=au)
        response = view(request, pk=o.id)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getby_userid(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        au = User.objects.create_user("authuser", "test@example.fr","fakepass")
        o = Organization(name="supO",contact="con@ex.fr",owner=u)
        o.save()

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('orga-list'),{"userid":u.id})
        force_authenticate(request, user=au)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(response.data['results'][0]['id'],1)
        self.assertIs(response.data['results'][1]['id'],3)

        view = OrganizationViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('orga-list'),{"userid":9})
        force_authenticate(request, user=au)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),0)

    def test_get_indiv(self):
        User = get_user_model()
        u = User.objects.create_user("testuser", "test@example.fr","fakepass")
        au = User.objects.create_user("authuser", "test@example.fr","fakepass")
        o = Organization(name="supO",contact="con@ex.fr",owner=u)
        o.save()

        factory = APIRequestFactory()

        view = OrganizationViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('orga-list'),{"indiv":"true"})
        force_authenticate(request, user=au)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),2)

        view = OrganizationViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('orga-list'),{"indiv":"false"})
        force_authenticate(request, user=au)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),1)
