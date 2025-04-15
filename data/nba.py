from balldontlie import BalldontlieAPI

from keys import API_KEY

api = BalldontlieAPI(api_key=API_KEY)

def get_nba_games():
    """
    Fetches the list of NBA games for the 2024 season.
    """
    # Fetching games for the 2024 season
    games = api.nba.games.list(seasons=[2024]).data
    return games