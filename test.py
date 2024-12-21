from typing import List

from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.static.players import get_active_players
from nba_api.stats.static.teams import get_teams

teams: list = get_teams()
for team in teams:
    print(team)
