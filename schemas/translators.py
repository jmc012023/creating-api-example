from pydantic import BaseModel

class PartialTranslator(BaseModel):
    name: str

class CompleteTranslator(PartialTranslator):
    id: int
    name: str