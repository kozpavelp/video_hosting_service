"""Setting & configs"""
from envparse import Env

env = Env()

DB_URL = env.str(
    "DB_URL", default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)

TEST_DB_URL = env.str(
    "TEST_DB_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test",
)

ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALG: str = env.str("ALG", default="HS256")
