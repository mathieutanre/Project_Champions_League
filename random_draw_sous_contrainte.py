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

def initialize_constraints(teams):
    """
    Initialise et retourne les contraintes pour chaque club.
    """
    constraints = {}
    for pot in teams:
        for team in pot:
            constraints[team["club"]] = {
                "played": set(),
                "nationalities": {}
            }
    return constraints

def is_match_admissible(selected_team, home, away, constraints):
    """
    Vérifie si un match entre l'équipe à domicile et à l'extérieur est admissible.
    """
    if home["club"] in constraints[selected_team["club"]]["played"] or \
       home["nationality"] == selected_team["nationality"] or \
       constraints[home["club"]]["nationalities"].get(selected_team["nationality"], 0) >= 2:
        return False
    if away["club"] in constraints[selected_team["club"]]["played"] or \
       away["nationality"] == selected_team["nationality"] or \
       constraints[away["club"]]["nationalities"].get(selected_team["nationality"], 0) >= 2:
        return False

    return True

def update_constraints(selected_team, home, away, constraints, undo=False):
    """
    Met à jour ou annule la mise à jour des contraintes pour un match donné.
    """
    operation = -1 if undo else 1
    constraints[home["club"]]["played"].add(selected_team["club"]) if not undo else constraints[home["club"]]["played"].discard(selected_team["club"])
    constraints[selected_team["club"]]["played"].add(home["club"]) if not undo else constraints[selected_team["club"]]["played"].discard(home["club"])
    constraints[home["club"]]["nationalities"][selected_team["nationality"]] = constraints[home["club"]]["nationalities"].get(selected_team["nationality"], 0) + operation
    constraints[selected_team["club"]]["nationalities"][home["nationality"]] = constraints[selected_team["club"]]["nationalities"].get(home["nationality"], 0) + operation

    constraints[away["club"]]["played"].add(selected_team["club"]) if not undo else constraints[away["club"]]["played"].discard(selected_team["club"])
    constraints[selected_team["club"]]["played"].add(home["club"]) if not undo else constraints[selected_team["club"]]["played"].discard(away["club"])
    constraints[away["club"]]["nationalities"][selected_team["nationality"]] = constraints[away["club"]]["nationalities"].get(selected_team["nationality"], 0) + operation
    constraints[selected_team["club"]]["nationalities"][away["nationality"]] = constraints[selected_team["club"]]["nationalities"].get(away["nationality"], 0) + operation

def find_admissible_matches(selected_team, opponent_group, constraints):
    """
    Trouve et retourne tous les matchs admissibles pour une équipe sélectionnée.
    """
    admissible_matches = []
    for opponent1 in opponent_group:
        for opponent2 in opponent_group:
            if is_match_admissible(selected_team, opponent1, opponent2, constraints):
                admissible_matches.append((opponent1, opponent2))
            if is_match_admissible(selected_team, opponent2, opponent1, constraints):
                admissible_matches.append((opponent2, opponent1))
    return admissible_matches


def tirage_au_sort(selected_team, teams, opponent_group, constraints):
    """
    Sélectionne une combinaison admissible de matchs pour l'équipe sélectionnée dans tous les groupes.
    """
    all_matches = []
    for group in teams:
        if selected_team in group:
            continue  # Sauter le groupe de l'équipe sélectionnée
        admissible_matches = find_admissible_matches(selected_team, group, constraints)
        if not admissible_matches:
            return None  # Aucun match admissible trouvé, impossible de continuer
        # Sélectionne un match admissible au hasard
        match = random.choice(admissible_matches)
        all_matches.append(match)
        update_constraints(selected_team, *match, constraints)
    return all_matches

# Exemple d'utilisation
constraints = initialize_constraints(teams)
selected_team = teams[0][0]  # Exemple : sélectionner la première équipe du premier groupe

# Trouver des matchs admissibles pour l'équipe sélectionnée
admissible_matches = select_admissible_matches(selected_team, teams, constraints)
if admissible_matches:
    print(f"Admissible matches for {selected_team['club']}:")
    for home, away in admissible_matches:
        print(f"{home['club']} (Home) vs {away['club']} (Away)")
else:
    print(f"No admissible matches found for {selected_team['club']}.")
