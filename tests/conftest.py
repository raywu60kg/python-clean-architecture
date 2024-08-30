from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.common.container import Container
from src.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    container = Container()
    app.state.container = container

    yield TestClient(app)
