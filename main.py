from math import ceil

from fastapi import FastAPI
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.static.players import get_active_players

from player_list_dto import PlayerListDTO
from util import get_all_player_ids

app = FastAPI()


total_players: int = len(get_active_players())
player_ids: list = get_all_player_ids()


# Returns all current NBA players via pagination
@app.get("/players")
def get_all_players(page: int = 1, players_per_page: int = 10) -> dict:
    current_page: int = 1
    next_page: int = 2
    previous_page: int = 0
    isLastPage: bool = False

    if page > 0 and page <= ceil(total_players / players_per_page):
        current_page = page
        if page == ceil(total_players / players_per_page):
            isLastPage = True
            next_page = None
        else:
            next_page = current_page + 1
    if current_page > 1:
        previous_page = current_page - 1

    players_with_full_info: list = []
    start: int = (current_page * players_per_page) - players_per_page
    end: int = current_page * players_per_page
    for id in player_ids[start:end]:
        response: CommonPlayerInfo = CommonPlayerInfo(id).get_dict()
        player_data: list = response["resultSets"][0]["rowSet"][0]

        player: PlayerListDTO = PlayerListDTO(
            player_id=player_data[0],
            first_name=player_data[1],
            last_name=player_data[2],
            birth_date=player_data[7],
            height=player_data[11],
            weight=player_data[12],
            season_exp=player_data[13],
            jersey=player_data[14],
            position=player_data[15],
            team_id=player_data[18],
            team_city=player_data[22],
            team_name=player_data[19],
        )

        players_with_full_info.append(player)

    return {
        "players": players_with_full_info,
        "currentPage": current_page,
        "nextPage": next_page,
        "previousPage": previous_page,
        "isLastPage": isLastPage,
        "totalPlayers": total_players,
    }
