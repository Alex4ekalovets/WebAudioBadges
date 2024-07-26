import os
from pathlib import Path, PurePath

ROOT_DIR = Path(os.getenv("ROOT_DIR", default=Path(__file__).parent)).resolve()

STATIC_PATH = "/static"
STATIC_DIR = ROOT_DIR / "static"

# Path to static files in web
ATTESTATION_RESULTS_PATH = STATIC_PATH + "/attestation_data"

# Static files results directory
ATTESTATION_DATA_DIR = Path(os.getenv("ATTESTATION_DATA_DIR",
                                      default=STATIC_DIR / "attestation_data"))


# Dir with templates
TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", default=ROOT_DIR / "templates"))
