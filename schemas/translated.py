from pydantic import BaseModel

class CompleteTranslated(BaseModel):
    t_id: int
    t_name: str
    b_id: int
    b_title: str