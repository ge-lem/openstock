from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import datetime

from basic_invitations.models import Invitation
from basic_invitations.app_settings import app_settings


class Command(BaseCommand):
    help = 'Delete old invitation'

    def handle(self, *args, **options):
        weeknot = timezone.now()-datetime.timedelta(days=app_settings.INVITATION_EXPIRY)
        Invitation.objects.filter(created__lt=weeknot).delete()
        Invitation.objects.filter(accepted=True).delete()

