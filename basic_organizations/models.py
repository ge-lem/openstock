from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Organization(models.Model):
    """
    Represent an organization of users
    ----------
    name : str
        Name of the organization
    contact : email
        email to contact the organization
    description : str
        description of the organization
    managers : User[]
        managers of the organization
    """
    name = models.CharField(max_length=60, unique=True)
    contact = models.EmailField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             related_name="myorganizations")
    managers = models.ManyToManyField(get_user_model(),blank=True, related_name="organizations")
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='name_unique',
            ),
        ]
