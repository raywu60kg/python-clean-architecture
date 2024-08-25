from fastapi import FastAPI

from src.adapter.inward.web.router import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()
