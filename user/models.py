from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extrafields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extrafields)
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self, email, username, password = None, **extrafields):
        extrafields.setdefault('is_staff', False)
        extrafields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extrafields)
    
    def create_superuser(self, email, username, password = None, **extrafields):
        extrafields.setdefault('role', 'admin')
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)
        return self._create_user(email, username, password, **extrafields)
    
class User(AbstractBaseUser, PermissionsMixin):
    role_choices = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=role_choices, default='staff')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    