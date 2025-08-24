import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from api.main import app as fastapi_app


# Synchronous TestClient (FastAPI built-in)
@pytest.fixture(scope="module")
def client():
    with TestClient(fastapi_app) as c:
        yield c


# Asynchronous TestClient (httpx)
@pytest_asyncio.fixture(scope="module")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(fastapi_app),
        base_url="http://test",
    ) as ac:
        yield ac
