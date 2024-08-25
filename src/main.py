import asyncio

from fastapi import FastAPI

from src.adapter.inward.web.router import router
from src.common.container import Container


async def create_app() -> FastAPI:
    container = Container
    db = container.db()
    await db.create_database()
    app = FastAPI()
    app.include_router(router)
    app.state.container = container
    return app


app = asyncio.run(create_app())
