import requests
from pprint import pprint
import time 
BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
API ="I1oqQ0O4kOJdbR1jWRsRgSt9D2FdgezQ"

params = {
    "authkey": API,
    "data": "AP01"
}

for _ in range(10):  # 예시로 10번 호출
    response = requests.get(BASE_URL, params=params)
    time.sleep(1)

    pprint(response)