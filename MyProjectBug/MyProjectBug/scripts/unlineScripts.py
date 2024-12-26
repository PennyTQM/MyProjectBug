import os
import sys

import django

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProjectBug.settings")
django.setup()
from web.models import UserInfo

usr_obj = UserInfo.objects.filter(usr_name="1").first()
print(usr_obj)
