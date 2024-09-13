import os
from pathlib import Path

from Front.auth_app.models import User

ROOT_DIR = Path(os.getenv("ROOT_DIR", default=Path(__file__).parent)).resolve()

# Static url and dir
STATIC_URL = "/static"
STATIC_DIR = ROOT_DIR / "static"

# Dir with templates
TEMPLATES_DIR = [
    Path(ROOT_DIR / "templates"),
    Path(ROOT_DIR / "auth_app" / "templates"),
]

RECORDS_DIR = os.getenv("RECORDS_DIR")

# LDAP
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_DN = os.getenv("LDAP_DN")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
LDAP_USER_SEARCH_DN = os.getenv("LDAP_USER_SEARCH_DN")
LDAP_USER_SEARCH_FILTER = os.getenv("LDAP_USER_SEARCH_FILTER")

# MONGO
MONGODB_URL = os.getenv("ME_CONFIG_MONGODB_URL")

# LOGGING
LOGGER_NAME = "audio_badges"

BEANIE_MODELS = [User]
