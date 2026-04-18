from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_debug: bool = True
    app_secret_key: str = "dev-secret"
    rate_limit_free_per_day: int = 10
    rate_limit_pro_per_day: int = 500
    prompt_version: str = "v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
