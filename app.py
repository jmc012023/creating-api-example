from fastapi import FastAPI
from routers import books, translators, translated

app = FastAPI()

app.include_router(books.router)
app.include_router(translators.router)
app.include_router(translated.router)