from django.db import models
import uuid

class OnboardingObject(models.Model):
    # this sets a uuid as the primary id field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=500, null=False)
    address = models.CharField(max_length=1000, null=False)

    expenses_folder_id = models.CharField(max_length=500, null=False)
    owner_folder_id = models.CharField(max_length=500, null=False)
    property_folder_id = models.CharField(max_length=500, null=False)

    onboarding_start_date = models.DateField()
    launch_date = models.DateField()




