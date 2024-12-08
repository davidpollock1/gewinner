from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userAuth.urls')),
    path('', include('common.urls')),
    path('care_profiles/', include('care_profiles.urls', namespace='care_profiles')),
]
