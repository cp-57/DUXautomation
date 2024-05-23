from django.db import models
import uuid

class OnboardingObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    expenses_folder_id = models.CharField(max_length=500, null=True, blank=True)
    owner_folder_id = models.CharField(max_length=500, null=True, blank=True)
    property_folder_id = models.CharField(max_length=500, null=True, blank=True)

    onboarding_start_date = models.DateField(null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)




