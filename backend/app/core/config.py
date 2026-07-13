from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Obabueki Capital"

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()