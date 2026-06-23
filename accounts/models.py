from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django_jalali.db import models as jmodels

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        get_email = self.normalize_email(email)
        user = self.model(email=get_email, **kwargs)
        user.set_password(password)
        user.save()
        print('user created ')

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault("is_superuser", True)

        self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def generate_username(self):
        return self.email.split("@")[0]

    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER = [('woman', "woman"), ('man', 'man'), ('unSelected', "unSelected")]

    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=200, unique=True, db_index=True)
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    gender = models.CharField(
        max_length=100, choices=GENDER, default="unSelected")
    image_profile = models.ImageField(null=True, blank=True)
    banner = models.ImageField(null=True, blank=True)
    birth_day = jmodels.jDateField(null=True, blank=True)
    last_seen = jmodels.jDateTimeField()
    is_online = models.BooleanField(default=False)

    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-created_date", '-updated_date']
