import os
import sys

import django

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProjectBug.settings")
django.setup()
from web.models import PricePolicy,UserInfo



if __name__ == '__main__':
    data = {
        "category":1,
        "title":"个人免费使用",
        "price":0,
        "project_num":3,
        "project_member":2,
        "project_space":20,
        "per_file_size":5,

    }
    form = PricePolicy.objects.create(**data)
    form.save()
