from fastapi.templating import Jinja2Templates

from Front.config import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)

