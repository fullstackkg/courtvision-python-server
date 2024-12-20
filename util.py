import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Callable, List

from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.static.players import get_active_players

from players.player_summary import PlayerSummary

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_all_player_ids() -> List[int]:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    active_nba_players: List[dict] = await loop.run_in_executor(
        executor, get_active_players
    )
    return [player["id"] for player in active_nba_players]


async def get_player_info(player_id: int) -> PlayerSummary:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    try:
        get_info: Callable[[], CommonPlayerInfo] = partial(CommonPlayerInfo, player_id)
        common_player_info = await loop.run_in_executor(executor, get_info)
        response = await loop.run_in_executor(executor, common_player_info.get_dict)

        if not response.get("resultSets") or not response["resultSets"][0].get(
            "rowSet"
        ):
            return PlayerSummary()

        data = response["resultSets"][0]["rowSet"][0]

        return PlayerSummary(
            player_id=data[0],
            first_name=data[1],
            last_name=data[2],
            birth_date=data[7],
            height=data[11],
            weight=data[12],
            season_exp=data[13],
            jersey=data[14],
            position=data[15],
            team_id=data[18],
            team_city=data[22],
            team_name=data[19],
        )

    except Exception:
        return PlayerSummary()
