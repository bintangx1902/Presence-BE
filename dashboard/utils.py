import string, random
from django.contrib.auth.decorators import user_passes_test
import os


def generate_agency_code():
    letter = string.ascii_letters
    num = '0123456789'
    raw = letter + num
    return ''.join(random.sample(raw, 32))


def generate_qr_code():
    letter = string.ascii_letters
    num = '0123456789'
    raw = letter + num
    return ''.join(random.sample(raw, 24))


def generate_invitation_code():
    letter = string.ascii_letters
    num = '0123456789'
    raw = letter + num
    return ''.join(random.sample(raw, 16))


def is_registered(function=None, redirect_field_name='next', login_url='/'):
    decorator = user_passes_test(
        lambda u: u.user.agency is None,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator


def is_controller(function=None, redirect_field_name='next', login_url='/'):
    decorator = user_passes_test(
        lambda u: u.user.is_controller,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator
