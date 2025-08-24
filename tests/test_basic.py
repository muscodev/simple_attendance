

def test_basic_owner_login(client):
    response = client.get("/api/owner/login")
    print(client.base_url)
    assert response.status_code == 200
