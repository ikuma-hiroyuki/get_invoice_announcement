import os

import requests
from dotenv import load_dotenv


class RegistrationNumbsers:
    def __init__(self):
        self.number_list = []

    def get_number(self):
        with open("registration_numbers.csv", "r") as file:
            self.number_list = [_.replace("\n", "") for _ in file.readlines()]


register_number = RegistrationNumbsers()
register_number.get_number()


def get_invoice():
    load_dotenv()
    base_url = 'https://web-api.invoice-kohyo.nta.go.jp/1/num'
    register_number_list = register_number.number_list
    parameters = {
        "id": os.getenv("API_ID"),
        "number": register_number_list,
        "type": "21",
        "history": "0"
    }

    try:
        response = requests.get(base_url, params=parameters)
        response.raise_for_status()
        corporates = response.json()["announcement"]
    except requests.exceptions.RequestException as err:
        print("エラー: ", err)
    else:
        for corporate in corporates:
            print(f"[登録番号] {corporate['registratedNumber']}\n"
                  f"[名前] {corporate['name']}\n"
                  f"[住所] {corporate['address']}", end="\n\n")


if __name__ == "__main__":
    get_invoice()
