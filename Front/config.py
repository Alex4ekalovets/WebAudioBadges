import os
from pathlib import Path, PurePath

ROOT_DIR = Path(os.getenv("ROOT_DIR", default=Path(__file__).parent)).resolve()

STATIC_PATH = "/static"
STATIC_DIR = ROOT_DIR / "static"

# Dir with templates
TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", default=ROOT_DIR / "templates"))
# RECORDS_DIR = "/data/files"
RECORDS_DIR = r"\\Obmen\obmen\01.RUT\IT\Chekalovets\records"
