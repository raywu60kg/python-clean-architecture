from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient

from src.main import app


class TestCreateCustomer(IsolatedAsyncioTestCase):
    async def test_create_customer(self) -> None:
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.post("/accounts/send/{sourceAccountId}/{targetAccountId}/{amount}")
            assert response.status_code == 200
