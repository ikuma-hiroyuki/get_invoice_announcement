import csv
import os

import requests
from dotenv import load_dotenv

BASE_FILE_PATH = "registration_numbers.csv"
RESULT_FILE_PATH = "invoice.csv"
FIELDS = ['registratedNumber', 'name', 'address']


class APIRequest:
    def __init__(self, path):
        """
        CSVファイルのパスを受け取り、CSVファイルから登録番号のリストを読み込む
        ファイルが存在しない場合は FileNotFoundError がraise されて終了
        """
        with open(path) as file:
            self.number_list = [_.replace("\n", "") for _ in file.readlines()]

    def _get_request_params(self) -> dict:
        """
        発行するリクエストのパラメータを返す
        """
        return {
            "id": os.getenv("API_ID"),
            "number": self.number_list,
            "type": "21",
            "history": "0"
        }

    def get_response_json(self) -> int:
        """
        APIからのレスポンスを辞書のリストとしてインスタンス変数に格納する

        :return: レスポンスのステータスコード
        """
        base_url = "https://web-api.invoice-kohyo.nta.go.jp/1/num"
        response: requests.Response = requests.get(base_url, params=self._get_request_params())
        if response.status_code == 200:
            self.response_list = response.json()["announcement"]

        return response.status_code

    def wrete_csv(self, path, fields):
        """
        APIリクエストを発行し、結果をCSVファイルに書き込む
        :param path: 書き込むCSVファイルのパス
        :param fields: CSVファイルのフィールド名
        """
        with open(path, "w", encoding="utf-8", newline="") as file:
            write = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
            write.writeheader()
            write.writerows(self.response_list)


if __name__ == "__main__":
    load_dotenv()

    api_request = APIRequest(BASE_FILE_PATH)
    result = api_request.get_response_json()
    if result == 200:
        api_request.wrete_csv(RESULT_FILE_PATH, fields=FIELDS)
    else:
        print(f"APIリクエストに失敗しました status_code: {result}")
