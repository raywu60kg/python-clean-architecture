from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.common.container import Container
from src.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    container = Container()
    app.state.container = container
    with TestClient(app) as test_client:
        yield test_client
