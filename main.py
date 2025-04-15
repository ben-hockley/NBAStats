from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from datetime import datetime, timedelta

from data.nba import get_nba_games


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
        def __init__(self, full_name: str, abbreviation: str):
            self.full_name = full_name
            self.abbreviation = abbreviation

@app.get("/teams", response_class=HTMLResponse)
async def teams(request: Request):
    teams = [
        Team("Atlanta Hawks", "ATL"),
        Team("Boston Celtics", "BOS"),
        Team("Brooklyn Nets", "BKN"),
        Team("Charlotte Hornets", "CHA"),
        Team("Chicago Bulls", "CHI"),
        Team("Cleveland Cavaliers", "CLE"),
        Team("Dallas Mavericks", "DAL"),
        Team("Denver Nuggets", "DEN"),
        Team("Detroit Pistons", "DET"),
        Team("Golden State Warriors", "GSW"),
        Team("Houston Rockets", "HOU"),
        Team("Indiana Pacers", "IND"),
        Team("Los Angeles Clippers", "LAC"),
        Team("Los Angeles Lakers", "LAL"),
        Team("Memphis Grizzlies", "MEM"),
        Team("Miami Heat", "MIA"),
        Team("Milwaukee Bucks", "MIL"),
        Team("Minnesota Timberwolves", "MIN"),
        Team("New Orleans Pelicans", "NOP"),
        Team("New York Knicks", "NYK"),
        Team("Oklahoma City Thunder", "OKC"),
        Team("Orlando Magic", "ORL"),
        Team("Philadelphia 76ers", "PHI"),
        Team("Phoenix Suns", "PHX"),
        Team("Portland Trail Blazers", "POR"),
        Team("Sacramento Kings", "SAC"),
        Team("San Antonio Spurs", "SAS"),
        Team("Toronto Raptors", "TOR"),
        Team("Utah Jazz", "UTA"),
        Team("Washington Wizards", "WAS")
    ]
    return templates.TemplateResponse("teams.html", {"request": request, "teams": teams})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)