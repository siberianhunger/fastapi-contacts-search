import asyncio
import sqlite3
import re

from basic_logger import setup_logger
from config import settings
logger = setup_logger()
connection = sqlite3.connect(settings.db_name)


def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for f_line in file:
            yield f_line


def parse_separate_line(line: str) -> tuple[int, str] | None:
    try:
        str_id, raw_name = line.split(sep=';')
        return int(str_id), filter_name(raw_name)
    except ValueError as exc:
        logger.info(f"ValueError in parse_separate_line:{exc}\nthe line: {line}")
        return


def filter_name(input_string: str) -> str:
    # Using regular expression to keep only alphabet, numeric characters, parentheses, and hyphen
    filtered_string = re.sub(r'[^a-zA-Zа-яА-Я0-9()\- ’]', '', input_string.strip())
    return filtered_string


def insert_parsed_data(data: list[tuple[int, str]]):
    logger.info(f"{data[:10]}")
    connection.executemany(
        f'INSERT INTO {settings.query_table_name} VALUES (?,?)',
        data
    )
    connection.commit()


def init_sqlite_storage_if_not_exists():
    connection.execute(f'CREATE VIRTUAL TABLE IF NOT EXISTS {settings.query_table_name} USING fts5(id, name);')
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {settings.query_logs_table_name} (
    user_id TEXT,
    user_agent TEXT,
    accept_language TEXT,
    user_ip TEXT,
    query_body TEXT
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    connection.commit()


def process_data_from_file():
    buffer = []
    chunk_size = 100
    for line in read_large_file(settings.source_filename):
        p_line = parse_separate_line(line)
        if p_line:
            buffer.append(p_line)

        if len(buffer) >= chunk_size:
            insert_parsed_data(buffer)
            buffer = []

    if buffer:
        insert_parsed_data(buffer)
    connection.commit()

