from balldontlie import BalldontlieAPI

from keys import API_KEY

api = BalldontlieAPI(api_key=API_KEY)

class Team:
    def __init__(
            self,
            id: int,
            full_name: str,
            abbreviation: str,
            city: str,
            conference: str,
            division: str
            ):
        self.id = id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.city = city
        self.conference = conference
        self.division = division

NBA_teams = [
    Team(1, "Atlanta Hawks", "ATL", "Atlanta", "Eastern", "Southeast"),
    Team(2, "Boston Celtics", "BOS", "Boston", "Eastern", "Atlantic"),
    Team(3, "Brooklyn Nets", "BKN", "Brooklyn", "Eastern", "Atlantic"),
    Team(4, "Charlotte Hornets", "CHA", "Charlotte", "Eastern", "Southeast"),
    Team(5, "Chicago Bulls", "CHI", "Chicago", "Eastern", "Central"),
    Team(6, "Cleveland Cavaliers", "CLE", "Cleveland", "Eastern", "Central"),
    Team(7, "Dallas Mavericks", "DAL", "Dallas", "Western", "Southwest"),
    Team(8, "Denver Nuggets", "DEN", "Denver", "Western", "Northwest"),
    Team(9, "Detroit Pistons", "DET", "Detroit", "Eastern", "Central"),
    Team(10, "Golden State Warriors", "GSW", "San Francisco", "Western", "Pacific"),
    Team(11, "Houston Rockets", "HOU", "Houston", "Western", "Southwest"),
    Team(12, "Indiana Pacers", "IND", "Indianapolis", "Eastern", "Central"),
    Team(13, "Los Angeles Clippers", "LAC", "Los Angeles", "Western", "Pacific"),
    Team(14, "Los Angeles Lakers", "LAL", "Los Angeles", "Western", "Pacific"),
    Team(15, "Memphis Grizzlies", "MEM", "Memphis", "Western", "Southwest"),
    Team(16, "Miami Heat", "MIA", "Miami", "Eastern", "Southeast"),
    Team(17, "Milwaukee Bucks", "MIL", "Milwaukee", "Eastern", "Central"),
    Team(18, "Minnesota Timberwolves", "MIN", "Minneapolis", "Western", "Northwest"),
    Team(19, "New Orleans Pelicans", "NOP", "New Orleans", "Western", "Southwest"),
    Team(20, "New York Knicks", "NYK", "New York", "Eastern", "Atlantic"),
    Team(21, "Oklahoma City Thunder", "OKC", "Oklahoma City", "Western", "Northwest"),
    Team(22, "Orlando Magic", "ORL", "Orlando", "Eastern", "Southeast"),
    Team(23, "Philadelphia 76ers", "PHI", "Philadelphia", "Eastern", "Atlantic"),
    Team(24, "Phoenix Suns", "PHX", "Phoenix", "Western", "Pacific"),
    Team(25, "Portland Trail Blazers", "POR", "Portland", "Western", "Northwest"),
    Team(26, "Sacramento Kings", "SAC", "Sacramento", "Western", "Pacific"),
    Team(27, "San Antonio Spurs", "SAS", "San Antonio", "Western", "Southwest"),
    Team(28, "Toronto Raptors", "TOR", "Toronto", "Eastern", "Atlantic"),
    Team(29, "Utah Jazz", "UTA", "Salt Lake City", "Western", "Northwest"),
    Team(30, "Washington Wizards", "WAS", "Washington", "Eastern", "Southeast")
]

def get_nba_games(date : str):
    """
    Fetches the list of NBA games for the 2024 season.
    """
    # Fetching games for the 2024 season
    # Dates in the format YYYY-MM-DD
    games = api.nba.games.list(dates=[date]).data
    return games

def get_team_players(team_id : int):
    """
    Fetches the list of players for a given NBA team.
    """
    # Fetching players for the specified team
    players = api.nba.players.list(team_ids=[team_id], per_page=100).data
    return players

def get_team_games(team_id : int):
    """
    Fetches the list of games for a given NBA team on a specific date.
    """
    # Fetching games for the specified team and date
    games = api.nba.games.list(team_ids=[team_id], seasons=[2024], per_page=100).data
    return games