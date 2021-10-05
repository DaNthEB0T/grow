from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class GrowUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **other_fields):
        if not email:
            raise ValueError(_("Users must have an email address :--)"))

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            **other_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, user_name, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Staff must be assigned!"))  

        if other_fields.get('is_active') is not True:
            raise ValueError(_("Active must be assigned!"))  

        user = self.create_user(
            email=email,
            password=password,
            user_name=user_name,
            **other_fields
        )
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, user_name, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must be assigned!")) 

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Staff must be assigned!"))  

        if other_fields.get('is_active') is not True:
            raise ValueError(_("Active must be assigned!"))  

        user = self.create_user(
            email=email,
            password=password,
            user_name=user_name,
            **other_fields
        )
        return user


class GrowUser(AbstractBaseUser, PermissionsMixin):
    # Login Info
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    user_name = models.CharField(_("user name"), max_length=150, unique=True)

    # Personal Info
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    # Important Dates
    date_joined = models.DateTimeField(_("date joined"),auto_now_add=True)
    last_login = models.DateTimeField(_("last_login"),auto_now=True)

    # Permissions
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = GrowUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "first_name", "last_name"]
   

    def __str__(self):
        return self.user_name