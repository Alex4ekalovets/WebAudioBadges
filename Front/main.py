import logging

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from Front.auth_app.endpoints import auth_router
from Front.config import LOGGER_NAME, MONGODB_URL, BEANIE_MODELS
from Front.endpoints.endpoints import page_router
from Front import config
from contextlib import asynccontextmanager

logger = logging.getLogger(LOGGER_NAME)


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.database = app.mongodb_client.audio_badges
    await init_beanie(database=app.database, document_models=BEANIE_MODELS)
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        logger.info("Connected to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()


app = FastAPI(lifespan=db_lifespan, title="Transcriptions Comparison")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(config.STATIC_URL, StaticFiles(directory=config.STATIC_DIR), name="static")

app.include_router(page_router)
app.include_router(auth_router)
