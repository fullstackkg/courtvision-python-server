from typing import List, Optional

from pydantic import BaseModel

from players.player_list_dto import PlayerListDTO


class PlayerListResponse(BaseModel):
    players: List[PlayerListDTO]
    currentPage: int
    nextPage: Optional[int]
    previousPage: Optional[int]
    is_last_page: bool
    totalPlayers: int
