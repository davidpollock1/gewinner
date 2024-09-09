from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import TenantAwareModel

class CustomUser(TenantAwareModel, AbstractUser):
    pass
