from typing import Any, Dict, List

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_all_players(client: TestClient) -> None:
    page: int = 1
    players_per_page: int = 2
    response: Response = client.get(
        "/players", params={"page": page, "players_per_page": players_per_page}
    )
    assert response.status_code == 200
    data: Dict[str, Any] = response.json()

    players: List[Dict[str, Any]] = data["players"]
    assert players[0]["player_id"] == 1630173
    assert players[0]["first_name"] == "Precious"
    assert players[0]["last_name"] == "Achiuwa"

    assert players[1]["player_id"] == 203500
    assert players[1]["first_name"] == "Steven"
    assert players[1]["last_name"] == "Adams"

    assert data["currentPage"] == 1
    assert data["previousPage"] is None
    assert data["nextPage"] == 2
    assert len(data["players"]) == 2


def test_all_players_invalid_parameters(client: TestClient) -> None:
    page: int = 15
    players_per_page: int = 9999
    response: Response = client.get(
        "/players", params={"page": page, "players_per_page": players_per_page}
    )
    assert response.status_code == 200
    data: Dict[str, Any] = response.json()

    assert data["currentPage"] == 1
    assert data["previousPage"] is None
    assert data["nextPage"] == 2
    assert len(data["players"]) == 10
