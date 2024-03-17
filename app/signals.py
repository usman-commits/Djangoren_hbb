# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Broadband, DeviceRegistrationAnalytics

@receiver(post_save, sender=Broadband)
def update_device_registration_analytics(sender, instance, **kwargs):
    date = instance.Post_date.date()
    region = instance.Region
    device_type = instance.Device_type
    user = instance.user

    # Update or create analytics entry
    analytics_entry, created = DeviceRegistrationAnalytics.objects.get_or_create(
        date=date, region=region, device_type=device_type, user=user
    )

    if not created:
        analytics_entry.count += 1
        analytics_entry.save()
