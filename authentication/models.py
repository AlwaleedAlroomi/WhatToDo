from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .helpers import send_email_verification_email
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilePicture/%y/%m/%d', blank=True, null=False, default='profilePicture/24/01/11/default.jpeg')
    reset_password_token = models.CharField(max_length = 100, blank = True, null = True)
    email_verification_token = models.CharField(max_length = 100, blank = True, null = False)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return f'({self.id}) {self.user} profile'

@receiver(post_save, sender=User)
def _create_profile_receiver(instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        token = str(uuid.uuid4())
        profile.email_verification_token = token
        profile.save()
        send_email_verification_email(email=profile.user.email, token=token)
