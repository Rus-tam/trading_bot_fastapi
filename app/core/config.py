from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    base_url: str
    historical_kline_url: str
    websocket_url: str
    server_time_url: str
    api_key: str
    secret_key: str
    api_key_test: str
    secret_key_test: str
    base_websocket_url: str

    class Config:
        env_file = ".env"


settings = Settings()
