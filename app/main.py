from fastapi import FastAPI

from .routers import books


app = FastAPI()

app.include_router(books.router)

@app.get("/")
async def root():
    return {
        "message": "Hello FastAPI",
        "status": "Ok",
        100: None
        }