import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, List

from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.static.players import get_active_players

from players.player_list_dto import PlayerListDTO

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_all_player_ids() -> List[int]:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    active_nba_players: List[dict] = await loop.run_in_executor(
        executor, get_active_players
    )
    return [player["id"] for player in active_nba_players]


async def get_player_info(player_id: int) -> PlayerListDTO:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    get_info: Callable[[], CommonPlayerInfo] = partial(CommonPlayerInfo, player_id)

    common_player_info: CommonPlayerInfo = await loop.run_in_executor(
        executor, get_info
    )
    response: dict[str, Any] = await loop.run_in_executor(
        executor, common_player_info.get_dict
    )

    player_data: List[Any] = response["resultSets"][0]["rowSet"][0]
