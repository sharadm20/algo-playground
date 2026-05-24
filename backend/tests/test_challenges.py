from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import app

client = TestClient(app)

def test_get_solution_returns_code():
    resp = client.get("/api/challenges/two-sum/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["language"] == "java"
    assert "public class" in data["code"]

def test_get_solution_unknown_returns_404():
    resp = client.get("/api/challenges/nonexistent/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 404

def test_get_solution_blocks_dotdot_in_id():
    resp = client.get("/api/challenges/..%2f..%2fetc%2fpasswd/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 404

def test_get_solution_blocks_slash_in_id():
    resp = client.get("/api/challenges/etc/passwd/solution", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 404

def test_list_challenges_returns_array():
    resp = client.get("/api/challenges", headers={"X-Internal-Request": "true"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == "two-sum"
