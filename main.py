import sqlite3
from typing import Union, List, Dict, Annotated

from fastapi import FastAPI, Query, BackgroundTasks, Header, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse

from config import settings
from basic_logger import setup_logger
from txt_to_db_data_parser import init_sqlite_storage_if_not_exists, process_data_from_file

logger = setup_logger()
connection = sqlite3.connect(settings.db_name)
app = FastAPI()


@app.get("/search")
async def search(
        request: Request,
        background_tasks: BackgroundTasks,
        search_query: str = Query(min_length=3, max_length=50, pattern="^[a-zA-Z0-9]+$"),
        user_id: str = Header(None),
        user_agent: str = Header(None),
        accept_language: str = Header(None),

) -> JSONResponse:
    if not user_id:
        raise HTTPException(status_code=400, detail="User-ID header is missing")
    result = await get_contacts_by_name(search_query)
    background_tasks.add_task(
        log_query_info,
        user_id,
        user_agent,
        accept_language,
        request.client.host,
        search_query,
        str(result)
    )
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


async def get_contacts_by_name(name: str) -> List[Dict[int, str]]:
    contacts_from_query = []  # [Contact, ...]
    for row in connection.execute(f"SELECT id, name FROM {settings.query_table_name} WHERE name MATCH ?", (name,)):
        contacts_from_query.append({row[0]: row[1]})
    logger.info(f"query name: {name}\nids_from_query: {contacts_from_query}")
    return contacts_from_query


async def log_query_info(
        user_id: str,
        user_agent: str,
        accept_language: str,
        user_ip: str,
        query_body: str,
        query_result: str
):
    connection.execute(
        f'INSERT INTO {settings.query_logs_table_name} VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, user_agent, accept_language, user_ip, query_body, query_result)
    )
    connection.commit()


def storage_has_records():
    storage_row = [i for i in connection.execute(f"SELECT * FROM {settings.query_table_name} limit 1")]
    logger.info(f"storage_has_records query result: {storage_row}\n")
    return bool(storage_row)


@app.on_event("startup")
async def create_sqlite_tables():
    init_sqlite_storage_if_not_exists()
    if not storage_has_records():
        process_data_from_file()
