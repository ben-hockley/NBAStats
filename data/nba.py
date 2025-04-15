from balldontlie import BalldontlieAPI

from keys import API_KEY

api = BalldontlieAPI(api_key=API_KEY)
games = api.nba.games.list()