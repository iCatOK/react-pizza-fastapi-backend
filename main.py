from fastapi import FastAPI
from routers import users, test
import uvicorn

from database.config import engine, Base

app = FastAPI()
app.include_router(users.router)
app.include_router(test.router)


@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1')