import hmac
import hashlib
from urllib.parse import urlencode
from ...core.config import settings


class Crypto:
    def __init__(self):
        self.api_key = f"{settings.api_key}"
        self.secret_key = f"{settings.secret_key}"
