from fastapi.templating import Jinja2Templates

from web.config import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)

