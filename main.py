import asyncio
from math import ceil
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from players.player_list_dto import PlayerListDTO
from players.player_list_response import PlayerListResponse
from util import get_all_player_ids, get_player_info

app = FastAPI()


@app.get("/players", response_model=PlayerListResponse)
async def get_all_players(page: int = 1, players_per_page: int = 10) -> Dict[str, Any]:
    MAX_PLAYERS_PER_PAGE: int = 50
    MIN_PLAYERS_PER_PAGE: int = 1
    MIN_PAGE: int = 1
    MAX_PAGE: int = 615

    if (
        players_per_page < MIN_PLAYERS_PER_PAGE
        or players_per_page > MAX_PLAYERS_PER_PAGE
    ):
        players_per_page = 10  # Reset to default if outside valid range

    if page < MIN_PAGE or page > MAX_PAGE:
        page = 1  # Reset to first page if outside valid range

    # Get our player data with timeout protection
    try:
        player_ids: List[int] = await asyncio.wait_for(
            get_all_player_ids(), timeout=10.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Failed to retrieve player IDs within timeout period",
        )

    total_players: int = len(player_ids)
    total_pages: int = ceil(total_players / players_per_page)

    if page > total_pages:
        page = 1  # Reset to first page if the requested page exceeds available pages

    # Calculate pagination boundaries and metadata
    start: int = (page - 1) * players_per_page
    end: int = min(start + players_per_page, total_players)

    # Calculate navigation metadata
    is_last_page: bool = page == total_pages
    next_page: Optional[int] = None if is_last_page else page + 1
    previous_page: Optional[int] = None if page == 1 else page - 1

    # Fetch detailed information for the players on the current page
    try:
        player_tasks = [get_player_info(id) for id in player_ids[start:end]]
        players: List[PlayerListDTO] = await asyncio.wait_for(
            asyncio.gather(*player_tasks), timeout=15.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Failed to retrieve player details within timeout period",
        )

    # Construct the final response with all our validated and calculated data
    return PlayerListResponse(
        players=players,
        currentPage=page,
        nextPage=next_page,
        previousPage=previous_page,
        is_last_page=is_last_page,
        totalPlayers=total_players,
    )
