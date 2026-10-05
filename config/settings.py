from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ui_base_url: str = "https://the-internet.herokuapp.com"
    headless: bool = False
    route_base_url: str = "https://demo.playwright.dev/api-mocking"
    ui_username: str
    ui_password: SecretStr


settings = Settings()
