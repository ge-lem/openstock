from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

from basic_organizations.models import Organization

class PhotoPost(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             related_name="photos")
    image = models.ImageField(upload_to='posts')

    def __str__(self):
        return str(self.image)


class Post(models.Model):

    DRAFT = 2
    OPEN = 3
    CLOSED = 4
    EXPIRED = 5
    STATUS = (
        (DRAFT, ("draft")),
        (OPEN, ("open")),
        (CLOSED, ("closed")),
        (EXPIRED, ("expired")),
    )
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE,
                             related_name="posts")
    status = models.SmallIntegerField(choices=STATUS, default=DRAFT)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, default="Résumé\n\n\n---\n\n# Description\n")
    isRequest = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='posts', blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    update_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    tags = TaggableManager()
    
    def __str__(self):
        return str(self.title)
