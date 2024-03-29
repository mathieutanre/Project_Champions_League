import random
import pulp
import csv

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

def get_li_nationalities(teams):
    nationalities = set()
    for pot in teams:
        for team in pot:
            nationalities.add(team["nationality"])
    return nationalities


def get_index_of_team(team, teams):

    for i, pot in enumerate(teams):
        for j, t in enumerate(pot):
            if t['club'] == team:
                return i*9+j


    for i, pot in enumerate(teams):
        for j, t in enumerate(pot):
            if t == team:
                return i*9+j
    return None  # Si l'équipe n'est pas trouvée


def initialize_constraints(teams):
    all_nationalities = get_li_nationalities(teams) 
    constraints = {}
    for pot in teams:
        for team in pot:
            # Initialiser toutes les nationalités à 0 pour chaque équipe
            team_nationalities = {nat: 0 for nat in all_nationalities}
            # Ensuite, définir la nationalité de l'équipe courante à 2
            team_nationalities[team["nationality"]] = 2

            constraints[team["club"]] = {
                "played-home": set(),
                "played-ext": set(),
                "nationalities": team_nationalities
            }
    return constraints

def is_match_admissible(selected_team, home, away, constraints):
    """
    Vérifie si un match entre l'équipe à domicile et à l'extérieur est admissible.
    """
    if home["club"] == away["club"]:  #Sûreté
        return False
    if home["club"] in constraints[selected_team["club"]]["played-home"] or selected_team["club"] in constraints[home["club"]]["played-home"] or \
       home["club"] in constraints[selected_team["club"]]["played-ext"] or selected_team["club"] in constraints[home["club"]]["played-ext"] or \
       home["nationality"] == selected_team["nationality"] or \
       constraints[home["club"]]["nationalities"].get(selected_team["nationality"], 0) >= 2 or \
       constraints[selected_team["club"]]["nationalities"].get(home["nationality"], 0) >= 2:
        return False
    if away["club"] in constraints[selected_team["club"]]["played-home"] or selected_team["club"] in constraints[away["club"]]["played-home"] or \
       away["club"] in constraints[selected_team["club"]]["played-ext"] or selected_team["club"] in constraints[away["club"]]["played-ext"] or \
       away["nationality"] == selected_team["nationality"] or \
       constraints[away["club"]]["nationalities"].get(selected_team["nationality"], 0) >= 2 or \
       constraints[selected_team["club"]]["nationalities"].get(away["nationality"], 0) >= 2:
        return False

    return True

def find_admissible_matches(selected_team, opponent_group, constraints):
    """
    Trouve et retourne tous les matchs admissibles pour une équipe sélectionnée dans un groupe donnée.
    On vérifiera ensuite que ces couples peuvent ne pas aboutir à une impasse
    """
    admissible_matches = []
    for home in opponent_group:
        for away in opponent_group:
            if home != away and is_match_admissible(selected_team, home, away, constraints):
                admissible_matches.append((home, away))
    return admissible_matches

def update_constraints(home, away, constraints, add=True):
    # Mettre à jour les contraintes de rencontre pour le match entre home et away
    constraints[home["club"]]["played-home"].add(away["club"])
    constraints[away["club"]]["played-ext"].add(home["club"])
    
    # Mettre à jour les contraintes de nationalité pour le match entre home et away
    if add:
        constraints[home["club"]]["nationalities"][away["nationality"]] += 1
        constraints[away["club"]]["nationalities"][home["nationality"]] += 1
    else:
        constraints[home["club"]]["nationalities"][away["nationality"]] -= 1
        constraints[away["club"]]["nationalities"][home["nationality"]] -= 1


def write_to_csv(matches):
    with open("tirage_au_sort_1.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for match in matches:
            writer.writerow(match)


def solve_problem(selected_team, constraints, new_match, nationalities):
        # Création du problème
        name_prob = "Match_Schedule_" + str(random.random())
        prob = pulp.LpProblem(name_prob, pulp.LpMaximize)

        # Création du tableau pour stocker les variables de décision match_vars[i][j]=1 si i recoit j
        match_vars = [[pulp.LpVariable(f"Match_{i}_{j}", cat=pulp.LpBinary) for j in range(36)] for i in range(36)]

        #Fonction objectif nulle
        prob += 0

        # Contraintes globale

        # Contrainte : une équipe ne peut pas jouer contre elle-même
        for i in range(36):
            prob += match_vars[i][i] == 0

        # Contrainte : une équipe joue au plus 1 fois contre chaque autre équipe
        for i in range(36):
            for j in range(36):
                if i != j:
                    prob += pulp.lpSum(match_vars[i][j] + match_vars[j][i]) <= 1

        # Contraintes spécifiques pour chaque pot 1 match dom 1 match ext dans chaque pot
        for i in range(36):
            for pot_start in range(0, 36, 9):
                prob += pulp.lpSum(match_vars[i][j] for j in range(pot_start, pot_start + 9)) == 1
                prob += pulp.lpSum(match_vars[j][i] for j in range(pot_start, pot_start + 9)) == 1


        #Contrainte dans constraints
                
        # Ajouter la contrainte pour la paire de match a priori admissible
        home, away = new_match
        prob += match_vars[get_index_of_team(selected_team, teams)][get_index_of_team(home, teams)] == 1
        prob += match_vars[get_index_of_team(away, teams)][get_index_of_team(selected_team, teams)] == 1

        # Ajouter les contraintes dans constraints
        # Contraintes pour les matchs joués à domicile
        for pot in teams:
            for team in pot:
                for home_team in constraints[team['club']]["played-home"]:
                    prob += match_vars[get_index_of_team(team, teams)][get_index_of_team(home_team, teams)] == 1

        # Contraintes pour les matchs joués à l'extérieur
        for pot in teams:
            for team in pot:
                for away_team in constraints[team['club']]["played-ext"]:
                    prob += match_vars[get_index_of_team(away_team, teams)][get_index_of_team(team, teams)] == 1

        # Contraintes sur les nationalités
        for i in range(36):
            for j in range(36):
                if i != j:
                    # Si les équipes i et j ont la même nationalité, le match entre elles doit être impossible
                    if teams[i//9][i%9]["nationality"] == teams[j//9][j%9]["nationality"]:
                        prob += match_vars[i][j] == 0

        for nationality in nationalities:
            for i in range(36):
                prob += pulp.lpSum(match_vars[i][j]+match_vars[j][i] for j in range(36) if teams[j//9][j%9]["nationality"] == nationality) <= 2
            
        # Résolution du problème
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        if pulp.LpStatus[prob.status] == 'Optimal' :
            return True  
        else:
            return False  


def true_admissible_matches(teams, nationalities, selected_team, opponent_group, constraints):
    true_matches=list()
    admissible_matches = find_admissible_matches(selected_team, opponent_group, constraints)
    if not admissible_matches:
        print("La liste de match admissible avant vérification est vide")
        return None  # Aucun match admissible trouvé
    
    
    for match in admissible_matches:
        if solve_problem(selected_team, constraints, match, nationalities):
            true_matches.append(match)
    return true_matches



def tirage_au_sort(teams, constraints):
    '''Effectue le tirage au sort'''
    nationalities = get_li_nationalities(teams)
    matches_list = []
    for pot in range(4):
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(indices)
        for i in indices:
            selected_team = teams[pot][i]
            li_opponents=[teams[pot][i]["club"]]

            for idx_opponent_pot in range(4):
                matches_possible = true_admissible_matches(teams, nationalities, selected_team, teams[idx_opponent_pot], constraints)
                if not matches_possible:
                    continue
                (home, away) = random.choice(matches_possible)
                update_constraints(selected_team, home, constraints, add=True)
                update_constraints(away, selected_team, constraints, add=True)
                li_opponents.append((home["club"], away["club"]))
            print(li_opponents)
            matches_list.append(li_opponents)
    write_to_csv(matches_list)
    print("CSV file 'tirage_au_sort_1.csv' has been generated successfully.")




constraints = initialize_constraints(teams)

tirage_au_sort(teams, constraints)


