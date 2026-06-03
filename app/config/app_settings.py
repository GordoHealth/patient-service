from pydantic_settings import BaseSettings
from pydantic import SecretStr


class AppSettings(BaseSettings):
    """
        Add any general usage ENV variables and configuration functions below
    """

    ENVIRONMENT: str

    HIDE_HEALTHCHECK_LOGS: bool = True
    SECURE_BODY_LOGGING: bool = False
    DEVTOOLS_PASSWORD: SecretStr = SecretStr("")

app_settings = AppSettings()