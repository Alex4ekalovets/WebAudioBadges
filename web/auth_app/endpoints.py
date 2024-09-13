from typing import Annotated

from fastapi import APIRouter, Request, HTTPException, Form

from web.common import templates
from web.auth_app.utils import Auth

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@auth_router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@auth_router.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if await Auth(username, password).login():
        return {"message": "Successfully authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@auth_router.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if await Auth(username, password).register():
        return {"message": "Successfully registered"}
    else:
        raise HTTPException(status_code=401, detail=f"User with username '{username}' already exists")
