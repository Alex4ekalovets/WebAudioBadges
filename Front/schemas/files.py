from pydantic import BaseModel


class TextFile(BaseModel):
    record_number: str
    text: str
