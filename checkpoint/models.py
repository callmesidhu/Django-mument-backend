
from django.db import models

class Checkpoint(models.Model):
    email = models.EmailField()
    checkpoint = models.CharField(max_length=255)
    description = models.TextField()
    title = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True) 
    class Meta:
        db_table = "checkpoints"
    def __str__(self):
        return f"{self.title} - {self.email}"
