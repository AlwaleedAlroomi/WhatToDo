from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilePicture/%y/%m/%d', blank=True, null=False, default='profilePicture/24/01/11/default.jpeg')

    def __str__(self):
        return f'({self.id}) {self.user} profile'

@receiver(post_save, sender=User)
def _create_profile_receiver(instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
