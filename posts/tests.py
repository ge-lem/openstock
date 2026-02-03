from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from basic_organizations.serializers import OrganizationSerializer
from .models import Post

class DraftVisibilityTests(APITestCase):

    specificDraftContent = "a DRAFT with IMPROBABLE TiTLe"

    def setUp(self):
        self.user1InOrg = User.objects.create_user(username="user1inOrg", password="password")
        self.user1InOrg.save();
        self.org = OrganizationSerializer().create({'owner': self.user1InOrg, 'name': "org"})
        self.org.managers.add(self.user1InOrg)
        self.user2InOrg = User.objects.create_user("user2inOrg", "password")
        self.user2InOrg.save()
        self.org.managers.add(self.user2InOrg)
        self.org.save()
        self.user3NotInOrg = User.objects.create_user("user3notInOrg", "password")
        self.user3NotInOrg.save()
        self.post = Post.objects.create(
            status=Post.OPEN,
            owner=self.org,
            title="new POST",
            expire_date=timezone.now().date() + timedelta(days=1),
            update_user=self.user1InOrg,
        )
        self.draft = Post.objects.create(
            status=Post.DRAFT,
            owner=self.org,
            title=self.specificDraftContent,
            expire_date=timezone.now().date() + timedelta(days=1),
            update_user=self.user1InOrg,
        )

    def test_searchShowDraftToOrgMembers(self):
        url = reverse("searchpost-list")
        response = self.client.get(url)
        assert self.specificDraftContent not in str(response.content)
        self.client.force_login(self.user1InOrg)
        response = self.client.get(url)
        self.client.logout()
        assert self.specificDraftContent in str(response.content)
        self.client.force_login(self.user2InOrg)
        response = self.client.get(url)
        self.client.logout()
        assert self.specificDraftContent in str(response.content)
        self.client.force_login(self.user3NotInOrg)
        response = self.client.get(url)
        self.client.logout()
        assert self.specificDraftContent not in str(response.content)
