import csv
import os

import requests
from dotenv import load_dotenv

BASE_FILE_PATH = "registration_numbers.csv"
RESULT_FILE_PATH = "invoice.csv"
FIELD_DICT = {'registratedNumber': '登録番号', 'name': '名前', 'address': '住所', }


class APIRequest:
    def __init__(self, path):
        """
        CSVファイルのパスを受け取り、CSVファイルから登録番号のリストを読み込む
        """
        self.response_list = None
        with open(path) as file:
            self.number_list: list[str] = [_.strip() for _ in file.readlines()]

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
            self.response_list: list[dict] = response.json()["announcement"]

        return response.status_code

    def _rename_dict_keys(self, field_dict):
        """
        APIのレスポンスの辞書のキーを変換する

        :param field_dict: フィールドの辞書。変換前のキーをキー、変換後のキーを値とする
        :return: 変換後の辞書
        """
        for response_json in self.response_list:
            for old_key, new_key in field_dict.items():
                response_json[new_key] = response_json.pop(old_key)

    def write_csv(self, path, field_dict):
        """
        APIリクエストを発行し、結果をCSVファイルに書き込む
        :param path: 書き込むCSVファイルのパス
        :param field_dict: フィールドの辞書。 変換前のキーをキー、変換後のキーを値とする
        """
        self._rename_dict_keys(field_dict)

        with open(path, "w", encoding="utf-8", newline="") as file:
            write = csv.DictWriter(file, fieldnames=field_dict.values(), extrasaction="ignore")
            write.writeheader()
            write.writerows(self.response_list)


if __name__ == "__main__":
    load_dotenv()

    api_request: APIRequest = APIRequest(BASE_FILE_PATH)
    result: int = api_request.get_response_json()
    if result == 200:
        api_request.write_csv(RESULT_FILE_PATH, field_dict=FIELD_DICT)
    else:
        print(f"APIリクエストに失敗しました status_code: {result}")
