import hmac
import hashlib
from ...core.config import settings
import requests
import datetime
import json
import os


class Crypto:
    def __init__(self):
        self.api_key = f"{settings.api_key}"
        self.secret_key = f"{settings.secret_key}"

        self.api_key_test = f"{settings.api_key_test}"
        self.secret_key_test = f"{settings.api_key_test}"

        self.base_url = f"{settings.base_url}"

    # def generate_signature(self, params: dict):
    #     # Сортируем параметры по ключам
    #     query_string = urllib.parse.urlencode(sorted(params.items()))
    #     # Создаем подпись
    #     signature = hmac.new(
    #         self.secret_key_test.encode("utf-8"),
    #         query_string.encode("utf-8"),
    #         hashlib.sha256,
    #     ).hexdigest()

    #     return signature

    def generate_signature(self, params: dict) -> str:
        params_to_sign = (
            f"apiKey={params['apiKey']}&" f"timestamp={params['timestamp']}"
        )

        signature = hmac.new(
            key=self.secret_key.encode("utf-8"),
            msg=params_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return signature

    def generate_listen_key(self) -> str:
        file_name = "listen_key.json"
        url = f"{self.base_url}/api/v3/userDataStream"
        headers = {"X-MBX-APIKEY": self.api_key}

        if not os.path.isfile(file_name):
            print(f"Файл {file_name} не найден. Приступаю к созданию файла")

            default_data = {"listenKey": "", "timestamp": 0}

            with open(file_name, "w") as json_file:
                json.dump(default_data, json_file, indent=4, ensure_ascii=False)
            print(f"Файл {file_name} успешно создан")
        else:
            print(f"Файл {file_name} уже существует")

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Проверяем наличие ошибок
            listen_key = response.json().get("listenKey")
            current_time = datetime.datetime.now()
            data_to_json = {
                "listenKey": listen_key,
                "timestamp": int(current_time.timestamp() * 1000),
            }

            with open(file_name, "w") as json_file:
                json.dump(data_to_json, json_file, indent=4, ensure_ascii=False)

            return listen_key
        except requests.exceptions.RequestException as e:
            print("Error generating listenKey:", e)
            return None
