import os
from typing import Dict, List, Tuple

import sqlite3
# print(os.path.)
conn = sqlite3.connect(os.path.join("../storage", "portfolio.db"))
cursor = conn.cursor()


def _init_db():
    """Инициализирует БД"""
    with open("../sql/create_tables.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_create_tables():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT count(*) FROM sqlite_master "
                   "WHERE type='table'")
    table_exists = cursor.fetchall()[0][0]
    if int(table_exists) == 3:
        return
    _init_db()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


# check_db_exists()
check_create_tables()
