from fastapi import FastAPI
from routers.main import api_router
from settings import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(api_router,prefix=settings.API_V1_STR)

