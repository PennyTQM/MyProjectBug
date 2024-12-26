import hashlib
from django.conf import settings

def md5(string):
    m = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    m.update(string.encode('utf-8'))
    return m.hexdigest()