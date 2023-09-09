"""Setting & configs"""
from envparse import Env

env = Env()

DB_URL = env.str(
    "DB_URL", default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)
# ROMOTE IP FOR MIGRATIONS
# DB_URL = env.str("DB_URL", default="postgresql+asyncpg://postgres:postgres@146.70.149.217:5432/postgres")
TEST_DB_URL = env.str(
    "TEST_DB_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test",
)

ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALG: str = env.str("ALG", default="HS256")

SENTRY_URL = "https://5a3fb01ba8837fb4b77b347f6df306b7@o4505846124642304.ingest.sentry.io/4505846223732736"

PORT = env.int("PORT")
