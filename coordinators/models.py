from django.db import models
from django.contrib.postgres.fields import ArrayField

class Coordinator(models.Model):
    coordinator_email = models.EmailField(
        max_length=100,
        blank=True,     
        null=True,
        unique=True
    )

    
    players_email = ArrayField(
        models.EmailField(),
        blank=True,
        default=list,
        help_text="Array of player emails"
    )

    class Meta:
        db_table = "coordinators"

    def __str__(self):
        return self.coordinator_email  # fixed, no name field exists
