from nba_api.stats.static.players import get_active_players


def get_all_player_ids() -> list:
    active_nba_players: list = get_active_players()
    active_ids = []
    for player in active_nba_players:
        active_ids.append(player["id"])
    return active_ids
