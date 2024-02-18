from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api import notes, ping
from app.db import engine, metadata, SessionLocal
from prometheus_fastapi_instrumentator import Instrumentator

metadata.create_all(engine)

app = FastAPI()
instrumentator = Instrumentator().instrument(app)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


# @asynccontextmanager
# async def db():
#     try:
#         print("Connecting to database...")
#         await database.connect()
#         yield
#     finally:
#         print("Shutting down...")
#         await database.disconnect()

def get_db(request: Request):
    return request.app.state.db

@app.on_event("startup")
async def startup_event():
    instrumentator.expose(app)
    app.state.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.db.close()

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])

