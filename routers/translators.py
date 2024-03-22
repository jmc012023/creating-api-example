from fastapi import APIRouter
from models.translator import TranslatorModel
from schemas.translators import CompleteTranslator, PartialTranslator

router = APIRouter(
    prefix="/translators"
)

@router.get("/", status_code=200)
async def translators():
    translators = TranslatorModel.get_all()
    return translators

@router.get("/id/", status_code=200)
async def get_translator_id(id: int):
    translator = TranslatorModel.get_by_id(id)
    return translator

@router.get("/name/{name}", status_code=200)
async def get_translator_name(name: str):
    translators = TranslatorModel.get_by_name(name)
    return translators

@router.post("/", status_code=201)
async def new_translator(translator: PartialTranslator):
    new_translator = TranslatorModel.create(translator)
    return new_translator

@router.put("/update/")
async def update_translator(translator: CompleteTranslator):
    updated_translator = TranslatorModel.update(translator)
    return updated_translator

@router.delete("/")
async def delete_translator(id: int):
    deleted_translator = TranslatorModel.delete(id)
    return deleted_translator