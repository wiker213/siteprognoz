from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import SessionLocal, create_db_and_tables
from app.routes import all_routers
from app.services.users import ensure_default_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    db = SessionLocal()
    try:
        ensure_default_admin(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.api_title,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for r in all_routers:
    app.include_router(r)


@app.get("/")
def root():
    return {"status": "ok"}