from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class MumentUserManager(BaseUserManager):
    def create_user(self, email, name, domain, idea_submission, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, domain=domain, idea_submission=idea_submission)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, domain, idea_submission, password=None):
        user = self.create_user(email, name, domain, idea_submission, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MumentUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    domain = models.CharField(max_length=100)
    idea_submission = models.TextField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MumentUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'domain', 'idea_submission']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'mument_users'
