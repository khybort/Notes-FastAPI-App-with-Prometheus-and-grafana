import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz
from fastapi import Request

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed",String(8), default="False"),
    Column("created_date", String(50), default=dt.now(tz("Europe/London")).strftime("%Y-%m-%d %H:%M"))
)
# Databases query builder
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db(request: Request):
    return request.app.state.db
database = Database(DATABASE_URL)
