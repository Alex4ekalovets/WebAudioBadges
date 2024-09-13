import json
import logging

from ldap3 import Server, ALL, Connection
from passlib.context import CryptContext

from Front.config import (
    LDAP_SERVER,
    LDAP_DN,
    LDAP_PASSWORD,
    LDAP_USER_SEARCH_DN,
    LDAP_USER_SEARCH_FILTER,
    LOGGER_NAME,
)

logger = logging.getLogger(LOGGER_NAME)


class Auth:

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.auth_type = None

    def __get_password_hash(self) -> str:
        return self.__pwd_context.hash(self.password)

    def __get_hashed_user_password(self) -> str:
        return self.__pwd_context.hash(self.password)

    def __verify_password(self) -> bool:
        password = None
        return self.__pwd_context.verify(self.password, password)

    def __authenticate_ldap(self) -> bool:
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
        return True

    def __authenticate_no_ldap(self) -> bool:
        self.auth_type = "NO LDAP"
        return False

    def login(self) -> bool:
        if self.__authenticate_ldap() or self.__authenticate_no_ldap():
            logger.info(f"{self.auth_type}: User '{self.username}' successfully authenticated")
            return True
        return False

    def register(self):
        pass
