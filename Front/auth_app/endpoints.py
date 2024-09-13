from typing import Annotated

from fastapi import APIRouter, Request, HTTPException, Form

from Front.common import templates
from Front.auth_app.utils import Auth

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html")

@auth_router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(request, "register.html")

@auth_router.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if Auth(username, password).login():
        return {"message": "Successfully authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
