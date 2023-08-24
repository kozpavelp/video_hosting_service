"""Setting & configs"""

from envparse import Env

env = Env()

DB_URL = env.str(
    "DB_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)

TEST_DB_URL = env.str(
    "TEST_DB_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"
)
