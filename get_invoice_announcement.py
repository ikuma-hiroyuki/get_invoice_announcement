import csv
import os

import requests
from dotenv import load_dotenv

from get_registration_numbers import RegistrationNumbsers


def get_invoice_announcement() -> list[dict]:
    """
    インボイス公表システムWeb-APIから公表情報をjson形式で返却。\n

    インボイス公表システム(https://www.invoice-kohyo.nta.go.jp/)
    に登録番号を投げ公開情報を取得、json形式で返却。\n
    同階層の registration_numbers.csv に記載された番号を基に取得する。

    :rtype: list[dict]
    :return: インボイス公開情報をjsonで返す
    :raise: err: apiリクエスト失敗
    """

    register_numbers = RegistrationNumbsers()

    load_dotenv()
    parameters = {
        "id": os.getenv("API_ID"),
        "number": register_numbers.number_list,
        "type": "21",
        "history": "0"
    }

    try:
        base_url = 'https://web-api.invoice-kohyo.nta.go.jp/1/num'
        response: requests.Response = requests.get(base_url, params=parameters)
        response.raise_for_status()
        corporates: list[dict] = response.json()["announcement"]
    except requests.exceptions.RequestException as err:
        print("エラー: ", err)
    else:
        return corporates


def write_invoice_announcement(corporates: list[dict]):
    """
    json形式で渡された情報をもとに同階層に invoice.csv を作成する。\n
    :param list[dict] corporates:
    :return:
    """

    invoice_rows = [[
        corporate["registratedNumber"],
        corporate["name"],
        corporate["address"]
    ] for corporate in corporates]
    invoice_rows.insert(0, ["登録番号", "名前", "住所"])

    with open("invoice.csv", "w", encoding="utf-8", newline="") as file:
        csv.writer(file).writerows(invoice_rows)


if __name__ == "__main__":
    invoice_list: list[dict] = get_invoice_announcement()
    write_invoice_announcement(invoice_list)
