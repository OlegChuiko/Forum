from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.crypto import get_random_string


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)


@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):
    if not user.username:
        base_username = user.email.split('@')[0] if user.email else 'user'
        username = generate_unique_username(base_username)
        user.username = username
        user.save()

    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)


def generate_unique_username(base_username):
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username
