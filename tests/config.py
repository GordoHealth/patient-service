from pydantic_settings import SettingsConfigDict, BaseSettings


class TestDBSettings(BaseSettings):
    TEST_DATABASE_USER: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_HOST: str
    TEST_DATABASE_PORT: str
    TEST_DATABASE_NAME: str

    def database_url(self):
        return (
            f"postgresql://{self.TEST_DATABASE_USER}:{self.TEST_DATABASE_PASSWORD}"
            f"@{self.TEST_DATABASE_HOST}:{self.TEST_DATABASE_PORT}/{self.TEST_DATABASE_NAME}"
        )
    model_config = SettingsConfigDict(case_sensitive=True)


test_db_config = TestDBSettings()
