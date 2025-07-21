import datetime
import sqlite3
from typing import Callable

import faker

from cyberfusion.ProftpdSupport.models import User
from cyberfusion.ProftpdSupport.settings import settings
from cyberfusion.ProftpdSupport.users import (
    create_proftpd_user,
    get_user,
    get_users_amount,
    get_expire_users_ids,
    delete_expire_users,
)


def test_create_proftpd_user(faker: faker.Faker) -> None:
    username = faker.user_name()
    password = faker.password()
    uid = faker.random_int()
    gid = faker.random_int()
    home_directory = faker.file_path(extension="")

    proftpd_user = create_proftpd_user(
        username=username,
        password=password,
        uid=uid,
        gid=gid,
        home_directory=home_directory,
    )

    assert proftpd_user.id
    assert proftpd_user.username == username
    assert proftpd_user.password == password
    assert proftpd_user.uid == uid
    assert proftpd_user.gid == gid
    assert proftpd_user.home_directory == home_directory
    assert proftpd_user.shell_path == "/bin/false"
    assert proftpd_user.created_at


def test_get_proftpd_user(
    faker: faker.Faker, proftpd_factory: Callable[[], User]
) -> None:
    proftpd_user = proftpd_factory()

    user = get_user(proftpd_user.username)

    assert user.id == proftpd_user.id
    assert user.username == proftpd_user.username
    assert user.password == proftpd_user.password
    assert user.uid == proftpd_user.uid
    assert user.gid == proftpd_user.gid
    assert user.home_directory == proftpd_user.home_directory
    assert user.shell_path == proftpd_user.shell_path
    assert user.created_at == proftpd_user.created_at


def test_get_users_amount(
    faker: faker.Faker, proftpd_factory: Callable[[], User]
) -> None:
    assert get_users_amount() == 0

    proftpd_factory()

    assert get_users_amount() == 1


def test_get_expire_users_ids_none(proftpd_factory: Callable[[], User]) -> None:
    proftpd_factory()

    assert get_expire_users_ids() == []


def test_get_expire_users_ids_any(
    proftpd_factory: Callable[[], User], cursor: sqlite3.Cursor
) -> None:
    proftpd_user = proftpd_factory()

    created_at = proftpd_user.created_at - datetime.timedelta(
        hours=settings.user_expire_hours + 1
    )

    cursor.execute(
        "UPDATE `users` SET `created_at` = ? WHERE `id` = ?",
        (created_at, str(proftpd_user.id)),
    )

    assert get_expire_users_ids() == [proftpd_user.id]


def test_delete_expire_users(
    proftpd_factory: Callable[[], User], cursor: sqlite3.Cursor
) -> None:
    proftpd_user = proftpd_factory()

    assert get_users_amount() == 1

    created_at = proftpd_user.created_at - datetime.timedelta(
        hours=settings.user_expire_hours + 1
    )

    cursor.execute(
        "UPDATE `users` SET `created_at` = ? WHERE `id` = ?",
        (created_at, str(proftpd_user.id)),
    )

    assert get_expire_users_ids() == [proftpd_user.id]

    delete_expire_users()

    assert get_users_amount() == 0
