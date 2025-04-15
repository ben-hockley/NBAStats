from balldontlie import BalldontlieAPI

from keys import API_KEY

api = BalldontlieAPI(api_key=API_KEY)

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