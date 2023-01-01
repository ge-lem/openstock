import datetime


from django.db import models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.utils import timezone
from django.utils.crypto import get_random_string

from .app_settings import app_settings

class Invitation(models.Model):
    accepted = models.BooleanField(default=False)
    key = models.CharField(max_length=64, unique=True)
    sent = models.DateTimeField(null=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=True,
        max_length=app_settings.EMAIL_MAX_LENGTH,
    )
    created = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email, key=key, inviter=inviter, **kwargs
        )
        return instance

    def key_expired(self):
        expiration_date = self.created + datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY,
        )
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = get_current_site(request)
        invite_url = request.build_absolute_uri(app_settings.EMAIL_URL)
        ctx = kwargs
        ctx.update(
            {
                "invite_url": invite_url,
                "site_name": current_site.name,
                "email": self.email,
                "key": self.key,
                "inviter": self.inviter,
            },
        )
        try:
            email_template = "invitations/email/email_invite"

            subject = render_to_string(f"{email_template}_subject.txt", ctx)
            # remove superfluous line breaks
            subject = " ".join(subject.splitlines()).strip()
            subject = f"[{current_site.name}] "+subject

            bodies = {}
            template_name = f"{email_template}_message.txt"
            body = render_to_string(template_name, ctx).strip()
            msg = EmailMultiAlternatives(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
            )
            msg.send()
            self.sent = timezone.now()
            self.save()
        except:
            pass

    def __str__(self):
        return f"Invite: {self.email}"
