import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    response = await client.post(
        "/login", data={"username": test_user.email, "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
