import csv

matches = [[[(1, 8), (0, 8), (2, 0), (3, 8), (1, 1), (0, 1), (3, 4), (2, 7)],
            [(3, 3), (2, 2), (0, 2), (1, 6), (2, 8), (0, 0), (1, 4), (3, 5)], 
            [(1, 0), (3, 4), (0, 1), (1, 3), (2, 7), (2, 3), (3, 8), (0, 3)], 
            [(0, 4), (1, 4), (3, 1), (3, 7), (1, 0), (2, 4), (2, 6), (0, 2)], 
            [(0, 3), (1, 1), (2, 3), (0, 5), (3, 2), (3, 6), (1, 3), (2, 0)], 
            [(1, 6), (2, 8), (3, 5), (0, 4), (2, 2), (3, 1), (0, 6), (1, 2)], 
            [(2, 1), (0, 7), (1, 5), (2, 5), (3, 0), (1, 7), (0, 5), (3, 2)], 
            [(2, 4), (0, 6), (1, 2), (2, 6), (0, 8), (3, 3), (3, 7), (1, 8)], 
            [(3, 6), (0, 0), (1, 7), (2, 1), (0, 7), (1, 5), (2, 5), (3, 0)]], 
           [[(0, 2), (3, 7), (2, 2), (1, 8), (0, 3), (3, 4), (2, 3), (1, 1)], 
            [(1, 2), (0, 4), (2, 8), (2, 4), (0, 0), (3, 5), (3, 3), (1, 0)], 
            [(1, 1), (3, 8), (0, 7), (2, 7), (2, 0), (1, 3), (3, 2), (0, 5)], 
            [(2, 0), (3, 0), (1, 4), (0, 2), (3, 7), (1, 2), (0, 4), (2, 2)], 
            [(2, 5), (0, 3), (1, 3), (3, 2), (3, 6), (2, 1), (0, 1), (1, 5)], 
            [(3, 5), (2, 6), (0, 6), (3, 1), (1, 6), (0, 8), (2, 4), (1, 4)], 
            [(0, 5), (1, 7), (3, 4), (0, 1), (1, 5), (2, 5), (2, 7), (3, 6)], 
            [(3, 1), (1, 6), (0, 8), (3, 3), (2, 6), (0, 6), (1, 8), (2, 8)], 
            [(0, 0), (2, 3), (2, 1), (1, 0), (3, 8), (3, 0), (1, 7), (0, 7)]], 
           [[(1, 3), (2, 1), (0, 0), (3, 0), (1, 2), (0, 2), (2, 6), (1, 6)],
            [(0, 6), (2, 0), (1, 8), (0, 8), (3, 3), (1, 4), (2, 2), (3, 7)], 
            [(3, 4), (0, 1), (1, 0), (2, 3), (0, 5), (3, 2), (2, 1), (1, 3)], 
            [(3, 7), (1, 8), (0, 4), (2, 2), (2, 4), (0, 2), (1, 0), (3, 1)], 
            [(0, 7), (3, 6), (3, 8), (1, 1), (2, 3), (0, 3), (1, 5), (2, 5)], 
            [(1, 4), (3, 3), (2, 6), (0, 6), (3, 1), (1, 6), (0, 8), (2, 4)], 
            [(3, 2), (1, 5), (2, 5), (0, 7), (1, 7), (2, 7), (0, 3), (3, 8)], 
            [(2, 8), (3, 5), (3, 0), (1, 2), (0, 2), (2, 6), (1, 6), (0, 0)], 
            [(2, 7), (0, 5), (1, 1), (3, 4), (0, 1), (2, 0), (3, 6), (1, 7)]], 
           [[(3, 8), (1, 3), (2, 7), (2, 0), (0, 6), (1, 8), (3, 1), (0, 8)],
            [(1, 7), (3, 2), (0, 3), (1, 5), (2, 5), (0, 5), (3, 0), (2, 3)], 
            [(2, 6), (3, 1), (3, 3), (1, 4), (0, 4), (2, 2), (1, 2), (0, 6)], 
            [(0, 1), (2, 5), (3, 2), (1, 7), (2, 1), (0, 7), (1, 1), (3, 4)], 
            [(2, 2), (0, 2), (1, 6), (2, 8), (3, 5), (1, 0), (0, 0), (3, 3)], 
            [(1, 5), (2, 7), (0, 5), (3, 6), (3, 4), (1, 1), (2, 0), (0, 1)], 
            [(0, 8), (2, 4), (3, 7), (3, 5), (1, 4), (0, 4), (2, 8), (1, 6)], 
            [(2, 3), (1, 0), (3, 6), (0, 3), (1, 3), (3, 8), (0, 7), (2, 1)], 
            [(3, 0), (1, 2), (2, 4), (0, 0), (1, 8), (3, 7), (0, 2), (2, 6)]]]


remaining_teams = [[{"club": "Real Madrid", "nationality": "Spain"},
                    {"club": "Manchester City", "nationality": "England"},
                    {"club": "Bayern Munich", "nationality": "Germany"},
                    {"club": "Paris Saint-Germain", "nationality": "France"},
                    {"club": "Liverpool", "nationality": "England"},
                    {"club": "Atletico Madrid", "nationality": "Spain"},
                    {"club": "Barcelona", "nationality": "Spain"},
                    {"club": "Juventus", "nationality": "Italy"},
                    {"club": "Chelsea", "nationality": "England"}],
                   [{"club": "Borussia Dortmund", "nationality": "Germany"},
                    {"club": "Ajax", "nationality": "Netherlands"},
                    {"club": "Inter Milan", "nationality": "Italy"},
                    {"club": "RB Leipzig", "nationality": "Germany"},
                    {"club": "AC Milan", "nationality": "Italy"},
                    {"club": "Sevilla", "nationality": "Spain"},
                    {"club": "Arsenal", "nationality": "England"},
                    {"club": "Lazio", "nationality": "Italy"},
                    {"club": "Manchester United", "nationality": "England"}],
                   [{"club": "Napoli", "nationality": "Italy"},
                    {"club": "Tottenham Hotspur", "nationality": "England"},
                    {"club": "Porto", "nationality": "Portugal"},
                    {"club": "Bayer Leverkusen", "nationality": "Germany"},
                    {"club": "Roma", "nationality": "Italy"},
                    {"club": "Zenit Saint Petersburg", "nationality": "Russia"},
                    {"club": "Leicester City", "nationality": "England"},
                    {"club": "Villarreal", "nationality": "Spain"},
                    {"club": "Wolfsburg", "nationality": "Germany"}],
                   [{"club": "Everton", "nationality": "England"},
                    {"club": "Leeds United", "nationality": "England"},
                    {"club": "AS Monaco", "nationality": "France"},
                    {"club": "Real Sociedad", "nationality": "Spain"},
                    {"club": "Fiorentina", "nationality": "Italy"},
                    {"club": "Crystal Palace", "nationality": "England"},
                    {"club": "West Ham United", "nationality": "England"},
                    {"club": "Celtic", "nationality": "Scotland"},
                    {"club": "Eintracht Frankfurt", "nationality": "Germany"}]]


teams = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def fill_teams(teams, remaining_teams, pot, i):
    if pot == 4: # no more team to place
        return True
    else:
        for team in remaining_teams[pot]: # test each possibility
            teams[pot][i] = team
            remaining_teams[pot].remove(team)
            for jour in range(8): # test compatibility with matches already planned
                pot_opp, num_opp = matches[pot][i][jour]
                if teams[pot_opp][num_opp] != 0:
                    opponent = teams[pot_opp][num_opp]
                    if team["nationality"] == opponent["nationality"]:
                        remaining_teams[pot].append(teams[pot][i])
                        teams[pot][i] = 0
                        return False
            i += 1
            if i == 9:
                i = 0
                pot = pot + 1
            if fill_teams(teams, remaining_teams, pot, i): # test if it enables to fill completely the grid
                return True
            else: # otherwise, we go back to the step before
                i -= 1
                if i == -1:
                    i = 8
                    pot -= 1
                remaining_teams[pot].append(teams[pot][i])
                teams[pot][i] = 0
        return False

fill_teams(teams, remaining_teams, 0, 0)


def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for group_index, group in enumerate(data):
            group_letter = chr(ord('A') + group_index)
            for team_index, team in enumerate(group):
                team_number = team_index + 1
                club_name = team['club']
                nationality = team['nationality']
                line = f"{group_letter}{team_number} : {club_name} ({nationality})"
                csvwriter.writerow([line])


write_to_csv(teams, 'teams.csv')
