from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# 自定義你的 create_user 方式
class user_manager(BaseUserManager):
    def create_user(self, account, password):
        if not account:
            raise ValueError("User must have a username.")

        user = self.model(account=account, is_active=True)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, account, password):
        user = self.create_user(account=account, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# 自定義你的 user table
class User(AbstractUser):
    """
    使用者資料表, 使用 Django 預設 AbstractUser, 配合 jwt
    """

    account = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    first_name = None
    last_name = None
    line_notify_status = models.BooleanField(default=False, null=False)
    line_notify_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = []
    objects = user_manager()

    class Meta:
        db_table = "system_user"
        ordering = ["id"]
        verbose_name_plural = "System User - 系統使用者資訊"

    def __str__(self):
        return f"{self.account}"
