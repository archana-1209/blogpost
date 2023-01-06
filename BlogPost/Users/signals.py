


from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(
			user=instance
			)
            
		print('Profile Created!')



