from django.urls import path
from .views import *

urlpatterns = [
    path('', onboarding_list, name='onboarding-list'),
    path('onboarding/new/', create_onboarding, name='create-onboarding'),
    path('onboarding/<uuid:id>/', onboarding_detail, name='onboarding-detail'),
    path('dashboard-step-two/', dashboard_step_two_view, name='dashboard-step-two'),
    path('dashboard-step-three/', dashboard_step_three_view, name='dashboard-step-three'),
    path('dashboard-step-four/', dashboard_step_four_view, name='dashboard-step-four'),
]