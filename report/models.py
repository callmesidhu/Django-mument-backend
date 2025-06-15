from django.db import models

class DailyUpdate(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(editable=False)
    email = models.EmailField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "daily_updates"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} ({self.uuid})"
