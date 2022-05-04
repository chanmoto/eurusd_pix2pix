from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)


def test_read_main():
    response = client.post(
        "/article/",
        data={
            "2022.3.3 14:00:00",
            "135",
            "134",
            "134",
            "134",
            "134",
            "134",
        }
    )
    print(response)
    assert response == 200
    assert response == "string3"
