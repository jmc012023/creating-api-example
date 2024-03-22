from pydantic import BaseModel

class PartialBook(BaseModel):
    isbn: str
    title: str

class CompleteBook(PartialBook):
    id: int