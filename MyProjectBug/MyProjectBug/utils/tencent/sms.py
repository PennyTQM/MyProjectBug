from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from django.conf import settings
import json

# 配置短信应用的 SDK AppID 以及 App Key
appid = 12345678  # 替换为你的 AppID
appkey = "abcdefgh"  # 替换为你的 AppKey

# 要发送短信的手机号码
phone_number = None

# 短信模板 ID，在腾讯云短信控制台中申请
def send_sms(phone_number, template_id, sms_params):
    # 初始化多号发送器

    appid = settings.TENCENT_SMS_APP_ID
    appkey = settings.TENCENT_SMS_APP_KEY
    sign = settings.TENCENT_SMS_SING
    ssender = SmsSingleSender(appid, appkey)

    try:
        # 发送短信
        result = ssender.send_with_param(86, phone_number, template_id, sms_params, sign=sign)


        # 解析结果，如果发送成功，则 result['result'] 为 0
        if result and 'result' in result:
            if result['result'] == 0:
                print("短信发送成功")
            else:
                print("短信发送失败，错误码:", result['result'])
                print("错误消息:", result['errmsg'])

    except HTTPError as e:
        print("HTTPError:", e)
        print("错误消息:", e.message)
    except Exception as e:
        print("Exception:", e)
