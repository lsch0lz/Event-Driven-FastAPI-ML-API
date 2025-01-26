from fastapi import FastAPI, HTTPException

from app.api.main import api_router
from app.core.db.db import create_db_and_tables

app = FastAPI()
app.include_router(api_router)


# TODO: Use LifeSpan instead of on_event
@app.on_event("startup")
def create_db_tables():
    create_db_and_tables()
