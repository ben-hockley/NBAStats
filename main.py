from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from datetime import datetime, timedelta

from data.nba import get_nba_games
from data.nba import get_team_players
from data.nba import get_team_games


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return RedirectResponse(url="/home")

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):  # Include the Request object
    return templates.TemplateResponse("home.html", {"request": request})  # Render the home.html template

@app.get("/redirectGames")
async def redirectGames():
    dateToday: str = datetime.today().strftime("%Y-%m-%d")
    return RedirectResponse(url=f"/games/{dateToday}")

@app.get("/games/{date}", response_class=HTMLResponse)
async def games(request: Request, date: str):
    games = get_nba_games(date)
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    dates = [(selected_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-3, 4)]

    return templates.TemplateResponse("games.html", {
        "request": request,
        "games": games,
        "dates": dates,
        "current_date": date
    })

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

@app.get("/teams", response_class=HTMLResponse)
async def teams(request: Request):
    teams = NBA_teams
    return templates.TemplateResponse("teams.html", {"request": request, "teams": teams})

@app.get("/teams/{team_id}", response_class=HTMLResponse)
async def team_details(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)
    return templates.TemplateResponse("team_details.html", {"request": request, "team": team})

@app.get("/teams/{team_id}/players", response_class=HTMLResponse)
async def team_players(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)
    players = get_team_players(team_id)
    return templates.TemplateResponse("team_players.html", {"request": request, "team": team, "players": players})

@app.get("/teams/{team_id}/games", response_class=HTMLResponse)
async def team_games(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)
    games = get_team_games(team_id)
    return templates.TemplateResponse("team_games.html", {"request": request, "team": team, "games": games})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)