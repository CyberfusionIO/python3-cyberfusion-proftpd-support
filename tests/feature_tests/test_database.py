import sqlite3
from typing import Generator

from cyberfusion.ProftpdSupport.database import (
    get_database_connection,
)


def test_get_database_connection(database: Generator[None, None, None]) -> None:
    assert isinstance(get_database_connection(), sqlite3.Connection)
