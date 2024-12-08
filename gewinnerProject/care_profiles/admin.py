from django.contrib import admin
from .models import Patient, Caregiver

admin.site.register(Patient)
admin.site.register(Caregiver)