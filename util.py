from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.static.players import get_active_players

from players.player_list_dto import PlayerListDTO


def get_all_player_ids() -> list:
    active_nba_players: list = get_active_players()
    return [player["id"] for player in active_nba_players]


def get_player_info(player_id: int) -> PlayerListDTO:
    response = CommonPlayerInfo(player_id).get_dict()
    player_data = response["resultSets"][0]["rowSet"][0]

    return PlayerListDTO(
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
