from django.conf import settings


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        return getattr(settings, self.prefix + name, dflt)

    @property
    def DEFAULT_DESCRIPTION(self):
        """Default text for the post description"""
        return self._setting("DEFAULT_DESCRIPTION", "Texte apparaissant que quand la personne clique sur l'annonce.\n")

    @property
    def DEFAULT_ORG_COMMENT(self):
        """Default text for the internal organization comment on post"""
        return self._setting("DEFAULT_ORG_COMMENT", "Commentaire visible seulement des membres de l'organisation.\n")

    @property
    def DEFAULT_ABSTRACT(self):
        """Default text for the post abstract"""
        return self._setting("DEFAULT_ABSTRACT", "Texte apparaissant sur la page de recherche.")

app_settings = AppSettings("POSTS_")
