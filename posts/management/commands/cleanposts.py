from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.conf import settings


import datetime

from posts.models import Post


class Command(BaseCommand):
    help = 'Clean posts (close and delete)'

    def handle(self, *args, **options):
        #close expired posts

        expposts=Post.objects.filter(status=3).filter(expire_date__lt=timezone.now())
        for post in expposts:
            context = { 'SITE_URL': settings.SITE_URL, 'post': post }
            subject = render_to_string(
                template_name='emails/closingpost_subject.txt',
                context=context
            ).strip()
            text_content = render_to_string(
                template_name='emails/closingpost_message.txt',
                context=context
            )
            html_content = render_to_string(
                template_name='emails/closingpost_message.html',
                context=context
            )
            msg = EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER, [post.owner.contact], reply_to=settings.NOTIFICATION_REPLYTO)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("fail to send notif to "+post.owner.contact)
        Post.objects.filter(status=3).filter(expire_date__lt=timezone.now()).update(status=5)
        #delete expired posts
        onemouth = timezone.now()-datetime.timedelta(days=30)
        Post.objects.filter(expire_date__lt=onemouth).delete()

