import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .utils import validate_uzbek_phone_number
from .managers import UserManager


class User(AbstractUser):
    class UserRole(models.TextChoices):
        BASE = 'base', _('base')
        ADMIN = 'admin', _('admin')

    class UserStatus(models.TextChoices):
        ACTIVE = 'active', _('active')
        BLOCKED = 'blocked', _('blocked')

    email = None
    username = None
    phone_number = models.CharField(max_length=13, validators=[validate_uzbek_phone_number],
                                    verbose_name=_("phone number"), unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, verbose_name=_('role'),
                            default=UserRole.BASE)
    status = models.CharField(max_length=10, choices=UserStatus.choices, verbose_name=_("status"),
                              default=UserStatus.ACTIVE)
    is_verified = models.BooleanField(default=False, verbose_name=_("verified"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.phone_number


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), )
    otp_code = models.CharField(max_length=6, null=True, blank=True, verbose_name=_('otp code'))
    otp_key = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name=_('otp key'))
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.otp_code}"
