from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from datetime import datetime, timedelta

from data.nba import get_nba_games
from data.nba import get_team_players
from data.nba import get_team_games
from data.nba import get_many_teams_games
from data.nba import get_standings
from data.nba import get_all_active_players
from data.nba import NBA_teams

from account.accounts import init_users_db
from account.accounts import insert_new_user
from account.accounts import check_password

from account.accounts import get_following_teams
from account.accounts import get_following_teams_ids

from account.accounts import follow_new_team
from account.accounts import unfollow_team

from account.current_user import current_user


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    init_users_db()
    return RedirectResponse(url="/home")

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):  # Include the Request object
    # Check if the user is signed in
    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("home.html", {"request": request, "current_user": user})  # Render the home.html template

@app.get("/redirectGames")
async def redirectGames():
    dateToday: str = datetime.today().strftime("%Y-%m-%d")
    return RedirectResponse(url=f"/games/{dateToday}")

@app.get("/games/{date}", response_class=HTMLResponse)
async def games(request: Request, date: str):
    games = get_nba_games(date)
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    dates = [(selected_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-3, 4)]

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("games.html", {
        "request": request,
        "games": games,
        "dates": dates,
        "current_date": date,
        "current_user": user,
    })

@app.get("/teams", response_class=HTMLResponse)
async def teams(request: Request):
    teams = NBA_teams

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("teams.html", {"request": request, "teams": teams, "current_user": user})

@app.get("/teams/{team_id}", response_class=HTMLResponse)
async def team_details(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("team_details.html", {"request": request, "team": team, "current_user": user})

@app.get("/teams/{team_id}/players", response_class=HTMLResponse)
async def team_players(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)
    players = get_team_players(team_id)

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("team_players.html", {"request": request, "team": team, "players": players, "current_user": user})

@app.get("/teams/{team_id}/games", response_class=HTMLResponse)
async def team_games(request: Request, team_id: int):
    team = next((team for team in NBA_teams if team.id == team_id), None)
    played_games, upcoming_games = get_team_games(team_id)

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("team_games.html", {"request": request, "team": team, "played_games": played_games, "upcoming_games": upcoming_games, "current_user": user})

# not currently in use (incomplete function)
@app.get("/standings", response_class=HTMLResponse)
async def standings(request: Request):
    standings = get_standings()
    return templates.TemplateResponse("standings.html", {"request": request, "standings": standings})

# not currently in use (incomplete function)
@app.get("/players", response_class=HTMLResponse)
async def players(request: Request):
    players = get_all_active_players()
    return templates.TemplateResponse("players.html", {"request": request, "players": players})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):

    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    return templates.TemplateResponse("register.html", {"request": request, "current_user": user})

@app.post("/register")
async def register_user(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    
    insert_new_user(username, password)
    
    return RedirectResponse(url="/home", status_code=303)

@app.post("/login")
async def login_user(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    login_success : bool = check_password(username, password)
    if login_success:
        current_user["signed_in"] = True
        current_user["username"] = username
        return RedirectResponse(url="/home", status_code=303)
    else:
        return RedirectResponse(url="/home", status_code=303)

@app.post("/logout")
async def logout_user(request: Request):
    current_user["signed_in"] = False
    current_user["username"] = None
    return RedirectResponse(url="/home", status_code=303)

# manage account page
@app.get("/myNBA/favorites", response_class=HTMLResponse)
async def favourites(request: Request):
    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None
    following_teams = get_following_teams(user)

    addable_teams = NBA_teams.copy()

    # remove followed teams from add team selection
    for team in addable_teams:
        for following_team in following_teams:
            if team.id == following_team.id:
                addable_teams.remove(team)
                break

    return templates.TemplateResponse("favorites.html", {"request": request, "current_user": user, "following_teams": following_teams, "addable_teams": addable_teams})

@app.get("/myNBA/favorites_games", response_class=HTMLResponse)
async def favorites_games(request: Request):
    if current_user["signed_in"]:
        user = current_user['username']
    else:
        user = None

    following_teams_ids = get_following_teams_ids(user)
    favorite_teams = get_following_teams(user)

    # Get the games for the teams the user is following 
    played_games, upcoming_games = get_many_teams_games(following_teams_ids)

    return templates.TemplateResponse("favorites_games.html", {"request": request, "current_user": user, "played_games": played_games, "upcoming_games": upcoming_games, "favorite_teams": favorite_teams})

@app.post("/addFavoriteTeam")
async def add_favorite_team(request: Request):
    form = await request.form()
    team_id = form.get("team_id")
    follow_new_team(current_user["username"], team_id)
    return RedirectResponse(url="/myNBA/favorites", status_code=303)

@app.post("/unFollowTeam")
async def unfollow_following_team(request: Request):
    form = await request.form()
    team_id = form.get("team_id")
    # Remove the team from the user's followed teams in the database
    unfollow_team(current_user["username"], team_id)
    # Redirect to the manage account page
    return RedirectResponse(url="/myNBA/favorites", status_code=303)




    return templates.TemplateResponse("favorites_games.html", {"request": request, "current_user": user, "games": games})
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)