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