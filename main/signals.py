from django.db.models.signals import post_save
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(pre_social_login)
def create_profile_on_social_login(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)