import csv
import os

import requests
from dotenv import load_dotenv

from get_registration_numbers import RegistrationNumbsers

BASE_URL = 'https://web-api.invoice-kohyo.nta.go.jp/1/num'


def get_invoice_announcement() -> list[dict]:
    register_numbers = RegistrationNumbsers()
    register_numbers.get_number_list()

    load_dotenv()
    parameters = {
        "id": os.getenv("API_ID"),
        "number": register_numbers.number_list,
        "type": "21",
        "history": "0"
    }

    try:
        response: requests.Response = requests.get(BASE_URL, params=parameters)
        response.raise_for_status()
        corporates: list[dict] = response.json()["announcement"]
    except requests.exceptions.RequestException as err:
        print("エラー: ", err)
    else:
        return corporates


def write_invoice_announcement(corporates: list[dict]):
    invoice_rows = [
        [
            corporate["registratedNumber"],
            corporate["name"],
            corporate["address"]
        ]
        for corporate in corporates
    ]
    invoice_rows.insert(0, ["登録番号", "名前", "住所"])

    with open("invoice.csv", "w", encoding="utf-8", newline="") as file:
        csv.writer(file).writerows(invoice_rows)


if __name__ == "__main__":
    invoice_list = get_invoice_announcement()
    write_invoice_announcement(invoice_list)
