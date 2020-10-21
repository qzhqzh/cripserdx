import datetime

from django.utils.timezone import utc


def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)
