import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from ldap3 import Server, ALL, Connection
from passlib.context import CryptContext

from web.auth_app.models import User, TokenData
from web.config import (
    LDAP_SERVER,
    LDAP_DN,
    LDAP_PASSWORD,
    LDAP_USER_SEARCH_DN,
    LDAP_USER_SEARCH_FILTER,
    LOGGER_NAME,
    JWT_SECRET_KEY,
)

logger = logging.getLogger(LOGGER_NAME)

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.auth_type = None

    def __get_password_hash(self) -> str:
        return self.__pwd_context.hash(self.password)

    def __verify_password(self, password) -> bool:
        return self.__pwd_context.verify(self.password, password)

    async def get_user(self):
        return await User.find_one(User.username == self.username)

    async def __authenticate_ldap(self) -> bool:
        server = Server(LDAP_SERVER, get_info=ALL)

        # Подключение к LDAP
        conn = Connection(server, user=LDAP_DN, password=LDAP_PASSWORD)
        if not conn.bind():
            logger.error(f"Error connecting to LDAP server: Invalid BASE credentials")
            return False

        # Поиск пользователя
        conn.search(
            search_base=LDAP_USER_SEARCH_DN,
            search_filter=LDAP_USER_SEARCH_FILTER % self.username,
        )
        entries = conn.entries
        if not entries:
            logger.warning(
                f"Error connecting to LDAP server: "
                f"No LDAP user '{LDAP_USER_SEARCH_DN} {LDAP_USER_SEARCH_FILTER % self.username}'"
            )
            return False

        # Попытка входа с пользовательским паролем
        user = json.loads(entries[0].entry_to_json())["dn"]
        user_conn = Connection(server, user=user, password=self.password)
        if not user_conn.bind():
            logger.info(
                f"Error connecting to LDAP server: Invalid user '{self.username}' password"
            )
            return False
        self.auth_type = "LDAP"
        await self.register()
        return True

    async def __authenticate_no_ldap(self) -> bool:
        user = await self.get_user()
        logger.debug(f"User: {user}")
        if user is None:
            return False
        if not self.__verify_password(user.password):
            return False
        self.auth_type = "NO LDAP"
        return True

    async def login(self) -> bool:
        if await self.__authenticate_ldap() or await self.__authenticate_no_ldap():
            logger.info(
                f"{self.auth_type}: User '{self.username}' successfully authenticated"
            )
            return True
        logger.debug(f"User '{self.username}' authentication fail")
        return False

    async def register(self):
        user = await self.get_user()
        if user is None:
            new_user = User(
                username=self.username, password=self.__get_password_hash()
            )
            await new_user.insert()
            logger.debug(f"Created new user '{new_user}'")
            return True
        logger.debug(f"User '{self.username}' already exists")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
