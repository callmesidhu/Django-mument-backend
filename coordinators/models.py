from django.db import models

class Coordinator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'coordinators'  

    def __str__(self):
        return self.name
