# pydantic has a utility BaseSettings which can help handle
# environment variables , explained in
# https://fastapi.tiangolo.com/advanced/settings/

from pydantic_settings import SettingsConfigDict, BaseSettings


class DBSettings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    def database_url(self):
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
    model_config = SettingsConfigDict(case_sensitive=True)


db_config = DBSettings()
