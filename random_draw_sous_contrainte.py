import random

teams = [[{"club": "ManCity", "nationality": "England"},
          {"club": "Bayern", "nationality": "Germany"},
          {"club": "Liverpool", "nationality": "England"},
          {"club": "Real", "nationality": "Spain"},
          {"club": "PSG", "nationality": "France"}, 
          {"club": "ManUnited", "nationality": "England"},
          {"club": "Barcelona", "nationality": "Spain"},
          {"club": "Inter", "nationality": "Italy"},
          {"club": "Sevilla", "nationality": "Spain"}],
         [{"club": "Dortmund", "nationality": "Germany"},
          {"club": "Atletico", "nationality": "Spain"},
          {"club": "Leipzig", "nationality": "Germany"},
          {"club": "Benfica", "nationality": "Portugal"},
          {"club": "Napoli", "nationality": "Italy"},
          {"club": "Porto", "nationality": "Portugal"},
          {"club": "Arsenal", "nationality": "England"},
          {"club": "Shakhtar", "nationality": "Ukraine"},
          {"club": "Salzburg", "nationality": "Austria"}],
         [{"club": "Atalanta", "nationality": "Italy"},
          {"club": "Feyenoord", "nationality": "Netherlands"},
          {"club": "Milan", "nationality": "Italy"},
          {"club": "Braga", "nationality": "Portugal"},
          {"club": "Eindhoven", "nationality": "Netherlands"},
          {"club": "Lazio", "nationality": "Italy"},
          {"club": "Crvena", "nationality": "Serbia"},
          {"club": "Copenhagen", "nationality": "Denmark"},
          {"club": "YB", "nationality": "Switzerland"}],
          [{"club": "Sociedad", "nationality": "Spain"},
           {"club": "Marseille", "nationality": "France"},
           {"club": "Galatasaray", "nationality": "Turkey"},
           {"club": "Celtic", "nationality": "Scotland"},
           {"club": "Qarabag", "nationality": "Azerbaijan"},
           {"club": "Newcastle", "nationality": "England"},
           {"club": "Berlin", "nationality": "Germany"},
           {"club": "Antwerp", "nationality": "Belgium"},
           {"club": "Lens", "nationality": "France"}]]

import random

def initialize_constraints(teams):
    constraints = {}
    for pot in teams:
        for team in pot:
            constraints[team["club"]] = {
                "played": set(),
                "nationalities": {team["nationality"]: float('inf')}  # Assure qu'une équipe ne joue pas contre sa propre nationalité
            }
    return constraints

def is_match_admissible(selected_team, home, away, constraints):
    if home["club"] == away["club"]:
        return False
    if home["club"] in constraints[selected_team["club"]]["played"] or away["club"] in constraints[selected_team["club"]]["played"]:
        return False
    if home["nationality"] == away["nationality"]:
        return False
    if constraints[home["club"]]["nationalities"].get(away["nationality"], 0) >= 2 or constraints[away["club"]]["nationalities"].get(home["nationality"], 0) >= 2:
        return False
    return True

def update_constraints(home, away, constraints, add=True):
    operation = (lambda x, y: x.add(y)) if add else (lambda x, y: x.discard(y))
    operation(constraints[home["club"]]["played"], away["club"])
    operation(constraints[away["club"]]["played"], home["club"])
    if add:
        constraints[home["club"]]["nationalities"][away["nationality"]] = constraints[home["club"]]["nationalities"].get(away["nationality"], 0) + 1
        constraints[away["club"]]["nationalities"][home["nationality"]] = constraints[away["club"]]["nationalities"].get(home["nationality"], 0) + 1
    else:
        constraints[home["club"]]["nationalities"][away["nationality"]] -= 1
        constraints[away["club"]]["nationalities"][home["nationality"]] -= 1

def backtrack_admissible_matches(opponent_group, constraints, matches=[], index=0):
    if index == len(opponent_group):
        return matches if len(matches) == len(opponent_group) * (len(opponent_group) - 1) / 2 else None
    
    for i, home in enumerate(opponent_group):
        for j, away in enumerate(opponent_group):
            if i != j and is_match_admissible(home, home, away, constraints):
                update_constraints(home, away, constraints)
                matches.append((home, away))
                
                result = backtrack_admissible_matches(opponent_group, constraints, matches, index + 1)
                if result:
                    return result
                
                matches.pop()
                update_constraints(home, away, constraints, add=False)
    
    return None



constraints = initialize_constraints(teams)
selected_team = teams[0][0]
opponent_group = teams[1]
result = backtrack_admissible_matches(opponent_group, constraints)

if result:
    print(f"Admissible matches for teams in the opponent group:")
    for home, away in result:
        print(f"{home['club']} (Home) vs {away['club']} (Away)")
else:
    print("No admissible matches configuration found without leading to a deadlock.")