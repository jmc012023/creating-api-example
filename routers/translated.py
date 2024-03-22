from fastapi import APIRouter
from models.translated import TranslatedModel

router = APIRouter(
    prefix="/translated"
)

@router.get("/", status_code=200)
async def show_all():
    info_translated = TranslatedModel.get_all()
    return info_translated
    
@router.get("/title/{title}")
async def filter_titles(title: str):
    result = TranslatedModel.get_by_title(title)
    return result

@router.get("/name/{name}", status_code=200)
async def filter_names(name: str):
    result = TranslatedModel.get_by_name(name)
    return result

@router.post("/")
async def create(b_id: int, t_id: int):
    new_translated = TranslatedModel.create_translated(b_id, t_id)
    return new_translated

@router.put("/update/translator/{new_t_id}")
async def update_translated_translator(new_t_id:int, b_id: int, t_id: int):
    updated_translated = TranslatedModel.update_translator(b_id, t_id, new_t_id)
    return updated_translated

@router.put("/update/book/{new_b_id}")
async def update_translated_book(new_b_id: int, t_id: int, b_id: int):
    updated_book = TranslatedModel.update_book(t_id, b_id, new_b_id)
    return updated_book

@router.delete("/delete/")
async def delete_translated(b_id: int, t_id: int):
    deleted_book = TranslatedModel.delete_by_book(b_id, t_id)
    return deleted_book