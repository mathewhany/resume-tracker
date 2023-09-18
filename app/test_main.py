from fastapi.testclient import TestClient
from .config import Config
from .main import app, get_config, get_metrics_manager

client = TestClient(app)


class FakeMetricsManager:
    def __init__(self):
        self.visits = {}

    def record_visit(self, page, source):
        if page not in self.visits:
            self.visits[page] = {}
        if source not in self.visits[page]:
            self.visits[page][source] = 0
        self.visits[page][source] += 1

    def get_all_counts(self):
        return self.visits


def test_main():
    metrics_manager = FakeMetricsManager()

    app.dependency_overrides = {
        get_metrics_manager: lambda: metrics_manager,
        get_config: lambda: Config(resume_url="https://example.com"),
    }

    response = client.get("/resume?source=google", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"
    assert metrics_manager.get_all_counts() == {"resume": {"google": 1}}

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == {"resume": {"google": 1}}

    response = client.get("/resume?source=google", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"
    assert metrics_manager.get_all_counts() == {"resume": {"google": 2}}

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == {"resume": {"google": 2}}

    response = client.get("/resume?source=bing", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"
    assert metrics_manager.get_all_counts() == {"resume": {"google": 2, "bing": 1}}

    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json() == {"resume": {"google": 2, "bing": 1}}
