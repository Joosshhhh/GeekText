from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, default='')
    phoneNum = models.IntegerField(default=0)


def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(createProfile, sender=User)
