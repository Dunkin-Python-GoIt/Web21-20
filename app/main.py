from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import books, auth


app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:5500",
    "127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(books.router, prefix="/api")
app.include_router(auth.router, prefix="/api")



@app.get("/")
async def root():
    return {
        "message": "Hello FastAPI",
        "status": "Ok",
        100: None
        }