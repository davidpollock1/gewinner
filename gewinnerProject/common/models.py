from django.db import models

class TenantAwareModel(models.Model):
    tenant_id = models.PositiveIntegerField()

    class Meta:
        abstract = True