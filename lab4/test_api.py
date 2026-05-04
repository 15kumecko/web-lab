from fastapi.testclient import TestClient
from lab2.main import app

client = TestClient(app)

def test_get_authors():
    response = client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_author():
    payload = {"id": 2, "name": "Test Author"}
    response = client.post("/authors", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Author"

def test_get_articles():
    response = client.get("/articles")
    assert response.status_code == 200

def test_create_and_delete_article():
    payload = {"id": 99, "author_id": 1, "title": "Test", "content": "Test text"}
    response_post = client.post("/articles", json=payload)
    assert response_post.status_code == 201
    
    article_id = response_post.json()["id"]
    response_delete = client.delete(f"/articles/{article_id}")
    assert response_delete.status_code == 204
