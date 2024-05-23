from django.contrib import admin

from .models import OnboardingObject

@admin.register(OnboardingObject)
class OnboardingObjectAdmin(admin.ModelAdmin):
    list_display = ('address', 'owner', 'onboarding_start_date', 'launch_date')
    search_fields = ('address', 'owner')
    list_filter = ('onboarding_start_date', 'launch_date')
