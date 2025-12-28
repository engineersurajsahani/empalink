from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import VolunteerProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_volunteer_profile(sender, instance, created, **kwargs):
    """
    Create a volunteer profile when a new user with volunteer role is created
    """
    if created and instance.role == 'volunteer':
        VolunteerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_volunteer_profile(sender, instance, **kwargs):
    """
    Save volunteer profile when user is saved
    """
    if hasattr(instance, 'volunteer_profile'):
        instance.volunteer_profile.save()