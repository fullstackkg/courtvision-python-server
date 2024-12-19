from math import ceil
from typing import Any, Dict, List, Optional

from fastapi import FastAPI

from util import get_all_player_ids, get_player_info

app = FastAPI()


@app.get("/players")
def get_all_players(page: int = 1, players_per_page: int = 10) -> Dict[str, Any]:
    MAX_PLAYERS_PER_PAGE: int = 50
    player_ids: List[int] = get_all_player_ids()
    total_players: int = len(player_ids)
    total_pages: int = ceil(total_players / players_per_page)

    if players_per_page < 1 or players_per_page > MAX_PLAYERS_PER_PAGE:
        players_per_page = 10
        page = 1
        total_pages = ceil(total_players / players_per_page)

    if page < 1:
        current_page: int = 1
    elif page > total_pages:
        current_page: int = total_pages
    else:
        current_page: int = page

    if current_page == total_pages:
        next_page: Optional[int] = None
    else:
        next_page: Optional[int] = current_page + 1

    if current_page == 1:
        previous_page: Optional[int] = None
    else:
        previous_page: Optional[int] = current_page - 1

    start: int = (current_page - 1) * players_per_page
    end: int = start + players_per_page

    players: List[Dict[str, Any]] = []
    for id in player_ids[start:end]:
        players.append(get_player_info(id))

    return {
        "players": players,
        "currentPage": current_page,
        "nextPage": next_page,
        "previousPage": previous_page,
        "is_last_page": current_page == total_pages,
        "totalPlayers": total_players,
    }
