import asyncio

from fastapi import FastAPI

from src.adapter.inward.web.router import router
from src.common.container import Container


async def create_app() -> FastAPI:
    container = Container
    db = container.db()
    if container.running_env != "test":
        await db.create_database()
    app = FastAPI()
    app.state.container = container
    app.include_router(router)
    return app


app = asyncio.run(create_app())
