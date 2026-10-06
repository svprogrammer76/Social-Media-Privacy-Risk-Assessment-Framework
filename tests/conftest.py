import pytest
from backend.app import app, init_db

@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setattr("backend.app.DB_PATH",tmp_path/"test.sqlite3")
    init_db(); app.config.update(TESTING=True)
    with app.test_client() as c: yield c
