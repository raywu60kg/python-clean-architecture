from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.adapter.inward.web.router import router
from src.common.container import Container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container = Container()
    database = container.database()
    await database.create_database()
    app.state.container = container
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
