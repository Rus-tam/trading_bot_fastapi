import hmac
import hashlib
from ...core.config import settings
import requests


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
        url = f"{self.base_url}/api/v3/userDataStream"
        headers = {"X-MBX-APIKEY": self.api_key}

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Проверяем наличие ошибок
            listen_key = response.json().get("listenKey")
            return listen_key
        except requests.exceptions.RequestException as e:
            print("Error generating listenKey:", e)
            return None
