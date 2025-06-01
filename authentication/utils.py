from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
import requests
from django.conf import settings
import random
import re
from datetime import timedelta

from django.utils import timezone


def generate_otp_code():
    return str(random.randint(100000, 999999))


def validate_uzbek_phone_number(value):
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid phone number. Format: +998938340101'))


def send_telegram_otp_code(otp):
    print(otp.otp_code)
    print(otp.user.phone_number)
    message = """P/j: Authentication\nPhone: {}\nOTP_code {}\nExpire in {}""".format(
        otp.user.phone_number, otp.otp_code, (otp.created_at + timedelta(minutes=3)).strftime('%H:%M:%S'))

    requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))


def check_otp(otp):
    first_otp = otp.first()

    if first_otp and timezone.now() - first_otp.created_at > timedelta(hours=12):
        otp.delete()

    if len(otp) > 2:
        raise ValidationError(_('To many attempts! Try again later.'))


def otp_expiring(value):
    if timezone.now() - value > timedelta(minutes=3):
        return True
    return False


def check_otp_attempts(otp, otp_code):
    if otp_expiring(otp.created_at):
        raise ValidationError(_('OTP is expired.'))

    if otp.attempts > 2:
        raise ValidationError(_('Too many attempts.'))

    if otp.otp_code != otp_code:
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        raise ValidationError(_('OTP code is incorrect.'))
    return otp
