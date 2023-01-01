from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    @property
    def INVITATION_EXPIRY(self):
        """How long before the invitation expires"""
        return self._setting("INVITATION_EXPIRY", 3)

    @property
    def EMAIL_MAX_LENGTH(self):
        """
        Adjust max_length of e-mail addresses
        """
        return self._setting("EMAIL_MAX_LENGTH", 254)

    @property
    def EMAIL_URL(self):
        """
        URL sent in the invitation email
        """
        return self._setting("EMAIL_URL", "/invitation")

    @property
    def INVITATION_LIMIT(self):
        """
        LIMIT of number of active invitation per user
        """
        return self._setting("INVITATION_LIMIT", 10)

    @property
    def INVITATION_ONESHOT(self):
        """
        Activation key can be checked only once
        If False you have to accept the Invitation manualy after you used it 
        or it can be used multiple times until it expires
        """
        return self._setting("INVITATION_ONESHOT", True)



app_settings = AppSettings("INVITATIONS_")
