import requests
from pprint import pprint
BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
API ="I1oqQ0O4kOJdbR1jWRsRgSt9D2FdgezQ"

params = {
    "authkey": API,
    "data": "AP01"
}

response = requests.get(BASE_URL, params=params)
data = response.json()
pprint(data)