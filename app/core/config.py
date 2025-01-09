from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    historical_kline_url: str
    websocket_url: str
    server_time_url: str

    class Config:
        env_file = ".env"


settings = Settings()
