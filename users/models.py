from django.db import models

class MumentUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    domain = models.CharField(max_length=100)
    idea_submission = models.TextField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "mument_users" 
