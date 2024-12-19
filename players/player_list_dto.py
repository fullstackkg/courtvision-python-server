from typing import ClassVar

from pydantic import BaseModel, computed_field


class PlayerListDTO(BaseModel):
    _teams: ClassVar[dict] = {
        "Hawks": {"conference": "Eastern", "division": "Southeast"},
        "Celtics": {"conference": "Eastern", "division": "Atlantic"},
        "Nets": {"conference": "Eastern", "division": "Atlantic"},
        "Hornets": {"conference": "Eastern", "division": "Southeast"},
        "Bulls": {"conference": "Eastern", "division": "Central"},
        "Cavaliers": {"conference": "Eastern", "division": "Central"},
        "Mavericks": {"conference": "Western", "division": "Southwest"},
        "Nuggets": {"conference": "Western", "division": "Northwest"},
        "Pistons": {"conference": "Eastern", "division": "Central"},
        "Warriors": {"conference": "Western", "division": "Pacific"},
        "Rockets": {"conference": "Western", "division": "Southwest"},
        "Pacers": {"conference": "Eastern", "division": "Central"},
        "Clippers": {"conference": "Western", "division": "Pacific"},
        "Lakers": {"conference": "Western", "division": "Pacific"},
        "Grizzlies": {"conference": "Western", "division": "Southwest"},
        "Heat": {"conference": "Eastern", "division": "Southeast"},
        "Bucks": {"conference": "Eastern", "division": "Central"},
        "Timberwolves": {"conference": "Western", "division": "Northwest"},
        "Pelicans": {"conference": "Western", "division": "Southwest"},
        "Knicks": {"conference": "Eastern", "division": "Atlantic"},
        "Thunder": {"conference": "Western", "division": "Northwest"},
        "Magic": {"conference": "Eastern", "division": "Southeast"},
        "76ers": {"conference": "Eastern", "division": "Atlantic"},
        "Suns": {"conference": "Western", "division": "Pacific"},
        "Trail Blazers": {"conference": "Western", "division": "Northwest"},
        "Kings": {"conference": "Western", "division": "Pacific"},
        "Spurs": {"conference": "Western", "division": "Southwest"},
        "Raptors": {"conference": "Eastern", "division": "Atlantic"},
        "Jazz": {"conference": "Western", "division": "Northwest"},
        "Wizards": {"conference": "Eastern", "division": "Southeast"},
        "None": {"conference": "N/A", "division": "N/A"},
    }

    player_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: str | None = None
    height: str | None = None
    weight: str | None = None
    season_exp: int | None = None
    jersey: str | None = None
    position: str | None = None
    team_id: int | None = None
    team_city: str | None = None
    team_name: str | None = None

    @computed_field
    @property
    def conference(self) -> str:
        team_name = self.team_name if self.team_name is not None else "None"
        return self._teams.get(team_name, self._teams["None"])["conference"]

    @computed_field
    @property
    def division(self) -> str:
        team_name = self.team_name if self.team_name is not None else "None"
        return self._teams.get(team_name, self._teams["None"])["division"]

    @computed_field
    @property
    def player_image_url(self) -> str:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{self.player_id}.png"

    @computed_field
    @property
    def team_image_url(self) -> str | None:
        print(self.team_id)
        if self.team_id is None or self.team_id == 0:
            return "https://cdn.worldvectorlogo.com/logos/nba-6.svg"
        return f"https://cdn.nba.com/logos/nba/{self.team_id}/global/L/logo.svg"
