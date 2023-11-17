from django.contrib.auth.models import BaseUserManager, UserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django.contrib.auth import get_user_model as usermd
