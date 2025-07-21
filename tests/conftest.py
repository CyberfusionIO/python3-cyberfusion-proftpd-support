import os
import shutil
import sqlite3
from pathlib import Path
from typing import Generator

import pytest
import faker
from pytest_mock import MockerFixture

from cyberfusion.ProftpdSupport.database import get_database_connection
from cyberfusion.ProftpdSupport.models import User
from cyberfusion.ProftpdSupport.users import create_proftpd_user
from cyberfusion.ProftpdSupport.settings import settings


@pytest.fixture(autouse=True)
def database(mocker: MockerFixture, tmp_path: Path) -> Generator[None, None, None]:
    original_database_path = settings.database_path

    tmp_database_path = os.path.join(str(tmp_path), "proftpd-support.db")

    shutil.copyfile(
        original_database_path,
        tmp_database_path,
    )

    settings.database_path = str(tmp_database_path)

    yield

    settings.database_path = original_database_path


@pytest.fixture
def proftpd_factory(faker: faker.Faker) -> User:
    def _create_proftpd_user() -> User:
        username = faker.user_name()
        password = faker.password()
        uid = faker.random_int()
        gid = faker.random_int()
        home_directory = faker.file_path(extension="")

        user = create_proftpd_user(
            username=username,
            password=password,
            uid=uid,
            gid=gid,
            home_directory=home_directory,
        )

        return user

    return _create_proftpd_user


@pytest.fixture
def connection(database: Generator[None, None, None]) -> sqlite3.Connection:
    return get_database_connection()


@pytest.fixture
def cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.cursor()
