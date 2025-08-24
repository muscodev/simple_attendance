import pytest


@pytest.mark.asyncio
async def test_async_owner_login(async_client):
    response = await async_client.get("/api/owner/login")
    assert response.status_code == 200
