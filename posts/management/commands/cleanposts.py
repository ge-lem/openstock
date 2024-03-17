from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import datetime

from posts.models import Post


class Command(BaseCommand):
    help = 'Clean posts (close and delete)'

    def handle(self, *args, **options):
        #close expired posts
        Post.objects.filter(status=3).filter(expire_date__lt=timezone.now()).update(status=5)
        #delete expired posts
        onemouth = timezone.now()-datetime.timedelta(days=30)
        Post.objects.filter(expire_date__lt=onemouth).delete()

