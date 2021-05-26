import json
import requests
import pandas as pd # 데이터프레임 사용을 위해
from math import log # IDF 계산을 위해
from konlpy.tag import Kkma
from konlpy.utils import pprint

def keyword_mining(question):

    url = 'http://svc.saltlux.ai:31781'

    headers = {'Content-Type': 'application/json; charset:utf-8'}

    params ={
        "key": "e87ac2a2-d4e3-48ca-9100-614f3fdba6df",
        "serviceId": "00116013830",
        'argument': {
            "question": question,
        }
    }

    response = json.loads(requests.post(url, headers=headers, data=json.dumps(params)).text)

    result = []
    k = 0
    for i in response['return_object']['keylists']:
        result.append(i['keyword'])
        k += 1
        if k == 5:
            break
    return result