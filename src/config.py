from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @staticmethod
    # def get_env_path():
    #     # Исправляет путь до конфигурации, если конфиг (.env) импортируется из jupiter-notebook
    #     root_path = os.path.abspath(os.curdir)
    #     if "src" == root_path.split("\\")[-1]:
    #         env_file = "../.env"
    #     else:
    #         env_file = ".env"
    #     return env_file

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
