import sqlite3
from typing import Union, Optional, List
from fastapi import FastAPI, Query, BackgroundTasks, Header, HTTPException, Request
from pydantic import BaseModel

from config import settings
from basic_logger import setup_logger

logger = setup_logger()
connection = sqlite3.connect(':memory:')
app = FastAPI()


class Contact(BaseModel):
    id: int
    name: str


@app.get("/search")
async def search(
        request: Request,
        background_tasks: BackgroundTasks,
        search_query: str = Query(..., description="The search query string"),
        user_id: str = Header,
        user_agent: str = Header(None),
        accept_language: str = Header(None),

) -> list[Contact] | None:
    if not user_id:
        raise HTTPException(status_code=400, detail="User-ID header is missing")
    result = await get_contacts_by_name(search_query)
    background_tasks.add_task(
        log_query_info,
        user_id,
        user_agent,
        accept_language,
        request.client.host,
        search_query
    )

    return result


async def get_contacts_by_name(name: str) -> list[Contact]:
    contacts_from_query = []  # [{ID: NAME}, ...]
    for row in connection.execute("SELECT id as u_id, name as u_name FROM contacts WHERE name MATCH ?", (name,)):
        print(row)
        contacts_from_query.append(Contact(id=row['u_id'], name=row['u_name']))
    logger.debug(f"query name: {name}\nids_from_query: {contacts_from_query}")
    return contacts_from_query


async def log_query_info(user_id: str, user_agent: str, accept_language: str, user_ip: str, query_body: str):
    connection.execute(
        f'INSERT INTO {settings.query_logs_table_name} VALUES (?, ?, ?, ?, ?)',
        (user_id, user_agent, accept_language, user_ip, query_body)
    )


@app.on_event("startup")
async def create_sqlite_tables():
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
