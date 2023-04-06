from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import DiscordOAuth2Manager


class DiscordUser(AbstractUser, PermissionsMixin):
    objects = DiscordOAuth2Manager()

    id = models.BigIntegerField(default=1110, primary_key=True)
    username = models.CharField(default="User", max_length=255, unique=True)
    avatar = models.CharField(blank=True, null=True, max_length=255)
    last_login = models.DateTimeField(auto_now_add=True)
    public_flags = models.BigIntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_authenticated = True
    backend = ""

    class Meta:
        ordering = ("username",)
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username