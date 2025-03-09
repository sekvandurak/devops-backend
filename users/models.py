from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UsersManager(BaseUserManager):
    def create_user(self, email, name, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.password = make_password(password)  # Explicitly hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, role, password=None, **extra_fields):
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(email, name, role, password, **extra_fields)

class Users(AbstractBaseUser):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    class Meta:
        db_table = 'Users'