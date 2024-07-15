import re
def load_data():
    """
    Load the data for the game and  returns a list of lists containing the  data.
    """
    result=[]
    with open("nba_game_warriors_thunder_20181016.txt") as game:
        content=game.read()
        for row in content.split('\n'):
            result.append(row.split('|'))
    return result

def get_team_player(game):
    """
    Extract players for each team from  game data.
    and returns two lists home containing home player's name and away containing the away player's one

    """
    li=[]
    home=[]
    away=[]
    for i in range(len(game)):
        player=re.search(r'([A-Z]\. [A-Z]\w+) (\w+)',game[i][7])
        if player and player.group(1) not in li:
            li.append(player.group(1))
            if game[i][2]==game[i][4]:
                home.append(player.group(1))
            elif game[i][2]==game[i][3]:
                away.append(player.group(1))

    for i in range(len(game)):
        player_=re.search(r'\w+ \w+ ([A-Z]\. [A-Z]\w+)',game[i][7])
        if player_:
            p=player_.group(1)
        if p not in li:
            li.append(p)
            if game[i][2]==game[i][4]:
                home.append(p)
            elif game[i][2]==game[i][3]:
                away.append(p)
    return home,away

def update_player_stats(move, player_stats):
    """
    Update player statistics based on a specific move in the NBA game.
    it takes a list representing a move in the NBA game data and a  dictionary representing the player's statistics and returns an Updated player statistics.
    """

    ast = re.search(r'assist by ([A-Z]. [A-Z]\w+)', move[7])
    stl = re.search(r'steal by ([A-Z]. [A-Z]\w+)', move[7])
    bk = re.search(r'block by ([A-Z]. [A-Z]\w+)', move[7])
    tov = re.search(r'Turnover by ([A-Z]. [A-Z]\w+)', move[7])
    pf = re.search(r'foul by ([A-Z]. [A-Z]\w+)', move[7])
    drb = re.search(r'Defensive rebound by ([A-Z]. [A-Z]\w+)', move[7])
    orb = re.search(r'Offensive rebound by ([A-Z]. [A-Z]\w+)', move[7])
    pattern = re.search(r'([A-Z]\. [A-Z]\w+) (\w+) ([0-9])-pt', move[7])
    free = re.search(r'([A-Z]\. [A-Z]\w+) (\w+) free', move[7])
    clear_free = re.search(r'([A-Z]\. [A-Z]\w+) makes clear path free', move[7])

    player_name = player_stats["player_name"]

    if ast and ast.group(1) == player_name:
        player_stats["AST"] += 1
    if stl and stl.group(1) == player_name:
        player_stats["STL"] += 1
    if bk and bk.group(1) == player_name:
        player_stats["BLK"] += 1
    if tov and tov.group(1) == player_name:
        player_stats["TOV"] += 1
    if pf and pf.group(1) == player_name:
        player_stats["PF"] += 1
    if drb and drb.group(1) == player_name:
        player_stats["DRB"] += 1
        player_stats["TRB"] += 1
    if orb and orb.group(1) == player_name:
        player_stats["ORB"] += 1
        player_stats["TRB"] += 1
    if pattern and pattern.group(1) == player_name:
        if pattern.group(2) == "makes":
            if pattern.group(3) == "2":
                player_stats["FG"] += 1
                player_stats["FGA"] += 1
                player_stats["PTS"] += 2
            elif pattern.group(3) == "3":
                player_stats["3P"] += 1
                player_stats["3PA"] += 1
                player_stats["FG"] += 1
                player_stats["FGA"] += 1
                player_stats["PTS"] += 3
        elif pattern.group(2) == "misses":
            if pattern.group(3) == "2":
                player_stats["FGA"] += 1
            elif pattern.group(3) == "3":
                player_stats["3PA"] += 1
                player_stats["FGA"] += 1

    if free and free.group(1) == player_name:
        if free.group(2) == "makes":
            player_stats["FT"] += 1
            player_stats["FTA"] += 1
            player_stats["PTS"] += 1
        else:
            player_stats["FTA"] += 1
    if clear_free and clear_free.group(1) == player_name:
        player_stats["FT"] += 1
        player_stats["FTA"] += 1
        player_stats["PTS"] += 1

    return player_stats

def get_team_stats(game, team_players):
    """
    Calculate statistics for each player in the team.

   inputs:
    game (list): A list of lists containing the NBA game data.
    team_players (list): A list of player names for a specific team.

    Returns:
    list: A list of dictionaries containing statistics for each player in the team.
    """
    team_stats = {player: {"player_name": player, "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0,
                           "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0,
                           "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
                  for player in team_players}
    for move in game:
        for player in team_players:
            if player in move[7]:
                team_stats[player] = update_player_stats(move, team_stats[player])

    for player_stats in team_stats.values():
        if player_stats["FTA"] != 0:
            player_stats["FT%"] = round(player_stats["FT"] / player_stats["FTA"], 3)
        if player_stats["3PA"] != 0:
            player_stats["3P%"] = round(player_stats["3P"] / player_stats["3PA"], 3)
        if player_stats["FGA"] != 0:
            player_stats["FG%"] = round(player_stats["FG"] / player_stats["FGA"], 3)

    return list(team_stats.values())

def analyse_nba_game(play_by_play_moves):
    """
    takes as input the moves 
    get statistics for teams
    and return a dictionnary summary of the game
    """
    res=get_team_player(play_by_play_moves)
    home_team_data=get_team_stats(play_by_play_moves,res[0])
    away_team_data=get_team_stats(play_by_play_moves,res[1])
    return {"home_team": {"name": play_by_play_moves[0][4], "players_data": home_team_data}, "away_team": {"name": play_by_play_moves[0][3], "players_data": away_team_data}}

def print_nba_game_stats(data_dict):
    headers = ["Players", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", 
               "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    
    # Print header row
    print("    " + "  ".join(headers))
    
    # Print player stats
    for player_data in data_dict["players_data"]:
        player_stats = [player_data["player_name"]]
        player_stats.extend([str(player_data[stat]) for stat in headers[1:]])
        print("    " + "   ".join(player_stats))
    
    # Calculate and print team totals
    team_totals = {stat: sum(player_data[stat] for player_data in data_dict["players_data"]) for stat in headers[1:]}
    if team_totals["FGA"] != 0:
        team_totals["FG%"] = round(team_totals["FG"] / team_totals["FGA"], 3)
    else:
        team_totals["FG%"] = 0.0
    if team_totals["3PA"] != 0:
        team_totals["3P%"] = round(team_totals["3P"] / team_totals["3PA"], 3)
    else:
        team_totals["3P%"] = 0.0
    if team_totals["FTA"] != 0:
        team_totals["FT%"] = round(team_totals["FT"] / team_totals["FTA"], 3)
    else:
        team_totals["FT%"] = 0.0

    team_totals_row = ["Team Totals"]
    team_totals_row.extend([str(team_totals[stat]) for stat in headers[1:]])
    print("    " + "   ".join(team_totals_row) + "\n")

data=load_data()
content=analyse_nba_game(data)
print_nba_game_stats(content["home_team"])





