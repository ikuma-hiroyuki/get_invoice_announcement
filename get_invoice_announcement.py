import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = 'https://web-api.invoice-kohyo.nta.go.jp/1/num'
corporate_list = ["T1000020028177", "T1000020035017", "T1010401013276", "T1000020038440"]
parameters = {
    "id": os.getenv("API_ID"),
    "number": corporate_list,
    "type": "21",
    "history": "0"
}

try:
    response = requests.get(BASE_URL, params=parameters)
    response.raise_for_status()
    corporates = response.json()["announcement"]
except requests.exceptions.RequestException as err:
    print("エラー: ", err)
else:
    for corporate in corporates:
        print(f"[登録番号] {corporate['registratedNumber']}\n"
              f"[名前] {corporate['name']}\n"
              f"[住所] {corporate['address']}", end="\n\n")
