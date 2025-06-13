import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class MumentUserManager(BaseUserManager):
    def create_user(self, email, name, phone, domain, idea_submission, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not name:
            raise ValueError("Name is required")
        if not phone:
            raise ValueError("Phone is required")
        if not domain:
            raise ValueError("Domain is required")
        if not idea_submission:
            raise ValueError("Idea submission is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            domain=domain,
            idea_submission=idea_submission,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class MumentUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    img_url = models.URLField(blank=True, null=True)
    mu_id = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    domain = models.CharField(max_length=100, blank=True, null=True)
    idea_submission = models.TextField()
    team = models.CharField(max_length=50, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    coordinator_id = models.IntegerField(blank=True, null=True)
    last_login = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone", "domain"]

    objects = MumentUserManager()

    class Meta:
        db_table = "mument_user_table"

    def __str__(self):
        return self.email
