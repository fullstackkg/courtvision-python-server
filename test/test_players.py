import asyncio
from typing import Any, Dict, List
from unittest.mock import patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from main import app
from players.player_list_dto import PlayerListDTO

# Mock data remains the same
MOCK_PLAYER_IDS = [1630173, 203500]

MOCK_PLAYERS = [
    PlayerListDTO(
        player_id=1630173,
        first_name="Precious",
        last_name="Achiuwa",
        birth_date="1999-09-19",
        height="6-8",
        weight="225",
        season_exp=2,
        jersey="5",
        position="F",
        team_id=1610612761,
        team_city="Toronto",
        team_name="Raptors",
    ),
    PlayerListDTO(
        player_id=203500,
        first_name="Steven",
        last_name="Adams",
        birth_date="1993-07-20",
        height="6-11",
        weight="265",
        season_exp=9,
        jersey="4",
        position="C",
        team_id=1610612763,
        team_city="Memphis",
        team_name="Grizzlies",
    ),
]


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_get_player_info():
    async def _mock_get_player_info(player_id: int) -> PlayerListDTO:
        for player in MOCK_PLAYERS:
            if player.player_id == player_id:
                return player
        raise ValueError(f"No player found with ID: {player_id}")

    return _mock_get_player_info


@pytest.fixture
def mock_get_all_player_ids():
    async def _mock_get_all_player_ids() -> List[int]:
        return MOCK_PLAYER_IDS

    return _mock_get_all_player_ids


@pytest.mark.asyncio
async def test_get_all_players(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch("main.get_all_player_ids", new=mock_get_all_player_ids), patch(
        "main.get_player_info", new=mock_get_player_info
    ):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 2}
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
        assert data["nextPage"] is None
        assert data["is_last_page"]
        assert len(data["players"]) == 2


@pytest.mark.asyncio
async def test_all_players_invalid_parameters(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch("main.get_all_player_ids", new=mock_get_all_player_ids), patch(
        "main.get_player_info", new=mock_get_player_info
    ):
        response: Response = client.get(
            "/players", params={"page": 15, "players_per_page": 9999}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert data["currentPage"] == 1
        assert data["previousPage"] is None
        assert data["nextPage"] is None
        assert data["is_last_page"]
        assert len(data["players"]) == 2


@pytest.mark.asyncio
async def test_min_players_per_page(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch("main.get_all_player_ids", new=mock_get_all_player_ids), patch(
        "main.get_player_info", new=mock_get_player_info
    ):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 1}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert len(data["players"]) == 1
        assert data["totalPlayers"] == len(MOCK_PLAYER_IDS)
        assert not data["is_last_page"]


@pytest.mark.asyncio
async def test_exact_max_players_per_page(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch("main.get_all_player_ids", new=mock_get_all_player_ids), patch(
        "main.get_player_info", new=mock_get_player_info
    ):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 50}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert len(data["players"]) == len(MOCK_PLAYER_IDS)
        assert data["is_last_page"]


@pytest.mark.asyncio
async def test_last_page_indicators(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch("main.get_all_player_ids", new=mock_get_all_player_ids), patch(
        "main.get_player_info", new=mock_get_player_info
    ):
        response: Response = client.get(
            "/players", params={"page": 2, "players_per_page": 1}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert data["currentPage"] == 2
        assert data["previousPage"] == 1
        assert data["nextPage"] is None
        assert data["is_last_page"]
