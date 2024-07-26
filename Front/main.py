from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from Front.endpoints.endpoints import page_router
from Front import config


app = FastAPI(title="Transcriptions Comparison")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(config.STATIC_PATH, StaticFiles(directory=config.STATIC_DIR))

app.include_router(page_router)


