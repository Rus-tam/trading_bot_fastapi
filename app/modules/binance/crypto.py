import hmac
import hashlib
from urllib.parse import urlencode
from ...core.config import settings


class Crypto:
    def __init__(self):
        self.api_key = f"{settings.api_key}"
        self.secret_key = f"{settings.secret_key}"

    def _generate_signature(self, params: dict) -> str:
        """
        Генерирует HMAC SHA256 подпись.
        """
        query_string = urlencode(params)
        return hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
