from pydantic import BaseModel

# STATS WE NEED TO GRAB
#  minutes: float
#     points: int
#     assists: int
#     off_reb: int
#     def_reb: int
#     reb: int
#     reb_pct: float
#     stl: int
#     blka: int
#     blk: int
#     tov: int
#     fga: int
#     fgm: int
#     fg_pct: float
#     fg3a: int
#     fg3m: int
#     fg3pct: float
#     fta: int
#     ftm: int
#     ft_pct: float
#     plus_minus: int
#     fouls: int


class PlayerStatsDTO(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    birth_date: str
    height: str
    weight: str
    season_exp: int
    school: str
    jersey: str
    position: str
    player_image_url: str

    team_id: int
    team_name: str
    conference: str
    division: str
    team_image_url: str
