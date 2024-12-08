from django.contrib import admin
from .models import CustomUser, Nurse

admin.site.register(CustomUser)
admin.site.register(Nurse)