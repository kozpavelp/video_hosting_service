import asyncio
import os
from typing import Any
from typing import Generator

import asyncpg
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import config
from app import app
from database.session import get_db


CLEAN_TABLES = ["users"]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system("alembic revision --autogenerate -m 'test running migrations'")
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
def async_session_test():
    engine = create_async_engine(config.TEST_DB_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean all table before running tests"""
    async with async_session_test() as session:
        async with session.begin():
            for table in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table};"))


async def _get_test_db():
    try:
        test_engine = create_async_engine(config.TEST_DB_URL, future=True, echo=True)
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(config.TEST_DB_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_db(asyncpg_pool):
    async def get_user_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM users WHERE user_id = $1;", user_id)

    return get_user_by_uuid


@pytest.fixture
async def create_user_in_db(asyncpg_pool):
    async def create_user_in_db(
        user_id: str, name: str, surname: str, email: str, is_active: bool
    ):
        async with asyncpg_pool.acquire() as conn:
            return await conn.execute(
                "INSERT INTO users VALUES ($1, $2, $3, $4, $5)",
                user_id,
                name,
                surname,
                email,
                is_active,
            )

    return create_user_in_db
