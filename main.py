from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from datetime import datetime, timedelta

from data.nba import get_nba_games
from data.nba import get_team_players
from data.nba import get_team_games
from data.nba import get_standings
from data.nba import NBA_teams


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
    played_games, upcoming_games = get_team_games(team_id)
    return templates.TemplateResponse("team_games.html", {"request": request, "team": team, "played_games": played_games, "upcoming_games": upcoming_games})

@app.get("/standings", response_class=HTMLResponse)
async def standings(request: Request):
    standings = get_standings()
    return templates.TemplateResponse("standings.html", {"request": request, "standings": standings})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)