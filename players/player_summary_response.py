from typing import List, Optional

from pydantic import BaseModel

from players.player_summary import PlayerSummary


class PlayerSummaryResponse(BaseModel):
    players: List[PlayerSummary]
    currentPage: int
    nextPage: Optional[int]
    previousPage: Optional[int]
    is_last_page: bool
    totalPlayers: int
