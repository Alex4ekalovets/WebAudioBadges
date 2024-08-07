import glob
import os
import re
import shutil

from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import FileResponse
from loguru import logger

import Front.config

from Front.common import templates

page_router = APIRouter()

DIRS = [d for d in os.listdir("/data/files")]
PAGE_FIRST_INDEXES = {1: 0}


@page_router.get("/")
def index(request: Request, page: int = 1):
    context = {"records": []}
    i = PAGE_FIRST_INDEXES.get(page, 0)
    items_on_page = 10
    count = 0
    while count < items_on_page:
        audio_file_name = f"{DIRS[i]}-audio.ogg"
        audio_file = f"/data/files/{DIRS[i]}/{audio_file_name}"
        text_file = f"/data/files/{DIRS[i]}/{DIRS[i]}-text.txt"
        if os.path.exists(audio_file) and os.path.getsize(audio_file) > 60000:
            with open(text_file, "r", encoding="cp1251") as f:
                text_1 = f.read()
            if len(text_1) != 0:
                transcription_pattern = re.compile(r"\bТранскрипция\b")
                time_pattern = re.compile(r"\d+:\d+")
                text_1 = transcription_pattern.sub("", text_1)
                text_1 = time_pattern.sub("", text_1)
                text_2_file = f"/data/files/{DIRS[i]}/{DIRS[i]}-text-whisper.txt"
                try:
                    with open(text_2_file, "r", encoding="cp1251") as f:
                        text_2 = f.read()
                except:
                    text_2 = ""
                record = {
                    "audio_file_name": audio_file_name,
                    "text_1": text_1.strip(),
                    "text_2": text_2,
                }
                context["records"].append(record)
                count += 1
        i += 1
    PAGE_FIRST_INDEXES[page + 1] = i
    if page >= 3:
        pages = [1, "...", page - 1, page, page + 1]
    else:
        pages = [1, 2, 3]
    context.update({"pages": pages})
    return templates.TemplateResponse(request, "index.html", context=context)


@page_router.get("/audio/{file_name}")
async def audio(request: Request, file_name: str):
    directory = file_name.split("-")[0]
    audio_file = f"/data/files/{directory}/{file_name}"
    audio_size = os.path.getsize(audio_file)
    headers = {
        "Content-Range": f"bytes=0-{audio_size}/{audio_size}",
        "Accept-Ranges": "bytes",
    }
    return FileResponse(audio_file, headers=headers, media_type="audio/wav")
