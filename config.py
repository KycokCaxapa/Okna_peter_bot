from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    ADMIN: int
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URL: str = ''

    def model_post_init(self, __context):
        if not self.DB_URL:
            self.DB_URL = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'


settings = Settings()
