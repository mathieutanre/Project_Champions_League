import random
import numpy as np
import csv
import random as rd
import copy


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


def init_graph(): 
    '''Renvoie la matrice de taille 36x36 avec None si le match est
       possible et 0 s'il est impossible (même nationalité et diagonale)'''
    graph = np.array([[None for _ in range(36)] for _ in range(36)])
    np.fill_diagonal(graph, 0)
    for pot in range(4):
        for i in range(9):
            team = teams[pot][i]
            for opponent_pot in range(4):
                for opponent_i in range(9):
                    opponent_team = teams[opponent_pot][opponent_i]
                    if team["nationality"] == opponent_team["nationality"]:
                        graph[9*pot+i, 9*opponent_pot+opponent_i] = 0
    return graph


def init_count_nationalities():
    '''retourne une liste de dictionnaires qui retient le nombre
    d'adversaires de chaque nationalité pour chaque équipe'''
    count_nationalities = []
    for _ in range(4):
        count_nationalities_pot = []
        for _ in range(9):
            dict = {"England": 0, "France": 0, "Germany": 0, "Italy": 0, "Portugal": 0, "Spain": 0,
                    "Serbia" : 0, "Switzerland" : 0, "Ukraine": 0, "Azerbaijan": 0, "Belgium": 0, 
                    "Netherlands": 0, "Scotland": 0, "Austria": 0, "Denmark": 0, "Turkey" : 0}
            count_nationalities_pot.append(dict)
        count_nationalities.append(count_nationalities_pot)
    return count_nationalities


def write_to_csv(matches):
    '''écrit les matchs dans un autre fichier'''
    with open("tirage_au_sort_1.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for match in matches:
            writer.writerow(match)


def updates_nationality(graph, count_nationalities, pot, i, nat):
    '''met des 0 partout où il ne peut plus y avoir de matchs après avoir
    choisi le match (pot, i)|(opponent_pot, opponent_i) pour satisfaire 
    la contrainte qu'une équipe ne peut affronter plus de 2 équipes d'un même pays'''
    if count_nationalities[pot][i][nat] == 2:
        for opponent_pot in range(4):
            for opponent_i in range(9):
                if teams[opponent_pot][opponent_i]["nationality"] == nat:
                    if graph[9*pot+i, 9*opponent_pot+opponent_i] != 1:
                        graph[9*pot+i, 9*opponent_pot+opponent_i] = 0
                    if graph[9*opponent_pot+opponent_i, 9*pot+i] != 1:
                        graph[9*opponent_pot+opponent_i, 9*pot+i] = 0


def updates_matches(graph, pot, i, opponent_pot, opponent_i):
    '''met des 0 partout où il ne peut plus y avoir de matchs après avoir
    choisi le match (pot, i)|(opponent_pot, opponent_i) pour satisfaire 
    la (2,2,2,2)-régularité'''
    graph[9*opponent_pot+opponent_i, 9*pot+i] = 0 # no return
    for k in range(9): # only one 1 in the line and in the column
        if k != opponent_i:
            graph[9*pot+i, 9*opponent_pot+k] = 0 
        if k != i:
            graph[9*pot+k, 9*opponent_pot+opponent_i] = 0


# def is_fillable(graph, count_nationalities):
#    def aux(graph, count_nationalities, pot, i, opponent_pot):
#        if pot == 4:
#            return True
#        else:
#            home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != 0]
#            away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != 0]
#            possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
#            nat = teams[pot][i]["nationality"]
#            for (home, away) in possible_matches:
#                new_graph = np.copy(graph)
#                new_count_nationalities = copy.deepcopy(count_nationalities)
#                if graph[9*pot+i, 9*opponent_pot+home] != 1: # match pas déjà tiré
#                    new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
#                    updates_matches(new_graph, pot, i, opponent_pot, home)
#                    nat_home = teams[opponent_pot][home]["nationality"]
#                    new_count_nationalities[pot][i][nat_home] += 1
#                    new_count_nationalities[opponent_pot][home][nat] += 1
#                    updates_nationality(new_graph, new_count_nationalities, pot, i, nat_home)
#                    updates_nationality(new_graph, new_count_nationalities, opponent_pot, home, nat)
#                if graph[9*opponent_pot+away, 9*pot+i] != 1:
#                    new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
#                    updates_matches(new_graph, opponent_pot, away, pot, i)
#                    nat_away = teams[opponent_pot][away]["nationality"]
#                    new_count_nationalities[pot][i][nat_away] += 1
#                    new_count_nationalities[opponent_pot][away][nat] += 1
#                    updates_nationality(new_graph, new_count_nationalities, pot, i, nat_away)
#                    updates_nationality(new_graph, new_count_nationalities, opponent_pot, away, nat) 
#                new_opponent_pot = (opponent_pot+1)%4
#                new_i = (i + new_opponent_pot==0)%9
#                new_pot = pot + new_i ==0           
#                if aux(new_graph, new_count_nationalities, new_pot, new_i, new_opponent_pot): # récursif
#                    return True
#            return False
#    return aux(graph, count_nationalities, 0, 0, 0)
            

def block_is_fillable(graph, count_nationalities, pot, opponent_pot):
    def aux(graph, count_nationalities, i):
        if i == 9:
            return True
        else:
            home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != 0]
            away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != 0]
            possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
            nat = teams[pot][i]["nationality"]
            for (home, away) in possible_matches:
                new_graph = np.copy(graph)
                new_count_nationalities = copy.deepcopy(count_nationalities)
                if graph[9*pot+i, 9*opponent_pot+home] != 1: # match pas déjà tiré
                    new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
                    updates_matches(new_graph, pot, i, opponent_pot, home)
                    nat_home = teams[opponent_pot][home]["nationality"]
                    new_count_nationalities[pot][i][nat_home] += 1
                    new_count_nationalities[opponent_pot][home][nat] += 1
                    updates_nationality(new_graph, new_count_nationalities, pot, i, nat_home)
                    updates_nationality(new_graph, new_count_nationalities, opponent_pot, home, nat)
                if graph[9*opponent_pot+away, 9*pot+i] != 1:
                    new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
                    updates_matches(new_graph, opponent_pot, away, pot, i)
                    nat_away = teams[opponent_pot][away]["nationality"]
                    new_count_nationalities[pot][i][nat_away] += 1
                    new_count_nationalities[opponent_pot][away][nat] += 1
                    updates_nationality(new_graph, new_count_nationalities, pot, i, nat_away)
                    updates_nationality(new_graph, new_count_nationalities, opponent_pot, away, nat)        
                if aux(new_graph, new_count_nationalities, i+1): 
                    return True
            return False
    return aux(graph, count_nationalities, 0)
            

def is_fillable(graph, count_nationalities):
    for pot in range(4):
        for opponent_pot in range(4):
            if not block_is_fillable(graph, count_nationalities, pot, opponent_pot):
                return False
    return True


def all_matches(graph, count_nationalities, pot, i, opponent_pot): 
    '''Retourne l'ensemble des matchs possibles entre l'équipe (pot, i) et les 
    équipes du pot opponent_pot en vérifiant récursivement qu'on peut compléter la matrice'''
    home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != 0]
    away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != 0]
    possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
    true_matches = []
    nat = teams[pot][i]["nationality"]
    for (home, away) in possible_matches:
        new_graph = np.copy(graph)
        new_count_nationalities = copy.deepcopy(count_nationalities)
        if graph[9*pot+i, 9*opponent_pot+home] != 1: # match pas déjà tiré
            new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
            updates_matches(new_graph, pot, i, opponent_pot, home)
            nat_home = teams[opponent_pot][home]["nationality"]
            new_count_nationalities[pot][i][nat_home] += 1
            new_count_nationalities[opponent_pot][home][nat] += 1
            updates_nationality(new_graph, new_count_nationalities, pot, i, nat_home)
            updates_nationality(new_graph, new_count_nationalities, opponent_pot, home, nat)
        if graph[9*opponent_pot+away, 9*pot+i] != 1:
            new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
            updates_matches(new_graph, opponent_pot, away, pot, i)
            nat_away = teams[opponent_pot][away]["nationality"]
            new_count_nationalities[pot][i][nat_away] += 1
            new_count_nationalities[opponent_pot][away][nat] += 1 
            updates_nationality(new_graph, new_count_nationalities, pot, i, nat_away)
            updates_nationality(new_graph, new_count_nationalities, opponent_pot, away, nat)         
        if is_fillable(new_graph, new_count_nationalities):
            true_matches.append((home, away))


def tirage_au_sort(graph, count_nationalities):
    '''Effectue le tirage au sort'''
    matches_list = []
    for pot in range(4):
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        rd.shuffle(indices)
        for i in indices:
            opponents = [teams[pot][i]["club"]] # juste pour affichage
            print(teams[pot][i])
            nat = teams[pot][i]["nationality"]
            for opponent_pot in range(4):
                print(all_matches(graph, count_nationalities, pot, i, opponent_pot))
                (home, away) = random.choice(all_matches(graph, count_nationalities, pot, i, opponent_pot))
                if graph[9*pot+i, 9*opponent_pot+home] != 1: # match pas déjà tiré
                    graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
                    updates_matches(graph, pot, i, opponent_pot, home)
                    nat_home = teams[opponent_pot][home]["nationality"]
                    count_nationalities[pot][i][nat_home] += 1
                    count_nationalities[opponent_pot][home][nat] += 1
                    updates_nationality(graph, count_nationalities, pot, i, nat_home)
                    updates_nationality(graph, count_nationalities, opponent_pot, home, nat)
                if graph[9*opponent_pot+away, 9*pot+i] != 1:
                    graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
                    updates_matches(graph, opponent_pot, away, pot, i)
                    nat_away = teams[opponent_pot][away]["nationality"]
                    count_nationalities[pot][i][nat_away] += 1
                    count_nationalities[opponent_pot][away][nat] += 1 
                    updates_nationality(graph, count_nationalities, pot, i, nat_away)
                    updates_nationality(graph, count_nationalities, opponent_pot, away, nat)  
                print((teams[opponent_pot][home]["club"], teams[opponent_pot][away]["club"]))        
                opponents.append((teams[opponent_pot][home]["club"], teams[opponent_pot][away]["club"]))
            print(opponents)
            matches_list.append(opponents)
    write_to_csv(matches_list)
    print("CSV file 'tirage_au_sort_1.csv' has been generated successfully.")


graph = init_graph()
count_nationalities = init_count_nationalities()
tirage_au_sort(graph, count_nationalities)