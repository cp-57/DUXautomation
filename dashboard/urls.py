from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard-step-one/', dashboard_step_one_view, name='dashboard-step-one'),
    path('dashboard-step-two/', dashboard_step_two_view, name='dashboard-step-two'),
    path('dashboard-step-three/', dashboard_step_three_view, name='dashboard-step-three'),
    path('dashboard-step-four/', dashboard_step_four_view, name='dashboard-step-four'),
]