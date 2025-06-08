def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Currency" in response.data or b"form" in response.data

def test_test_route(client):
    response = client.get("/test")
    assert response.status_code == 200
    assert b"Test successful" in response.data
