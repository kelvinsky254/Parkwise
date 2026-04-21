from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at fields.
    All Parkwise models inherit from this instead of models.Model directly.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
