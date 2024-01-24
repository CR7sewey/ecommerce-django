import string as s
from random import SystemRandom as SR
from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SR().choices(s.ascii_lowercase + s.digits, k=k))


def slugify_new(text, k=5):
    return slugify(text) + '-' + random_letters(k)
