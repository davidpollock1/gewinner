"""
URLS
"""
from django.urls import path
from . import views

app_name = 'care_profiles'

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    
    path('caregivers/', views.caregiver_list, name='caregiver_list'),
    path('caregivers/new/', views.caregiver_create, name='caregiver_create'),
    path('caregivers/<int:pk>/edit/', views.caregiver_update, name='caregiver_update'),
    
    path('care-plans/', views.care_plan_list, name='care_plan_list'),
    path('care-plan/new/', views.care_plan_create, name='care_plan_create'),
    path('care-plans/<int:pk>/', views.care_plan_update, name='care_plan_update'),
    
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/<int:pk>/', views.schedule_update, name='schedule_update'),
]
