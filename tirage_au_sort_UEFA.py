import random
import numpy as np


def possible_opponents(graph, pot, i, opponent_pot):
    home_opponents = []
    if np.sum(graph[9*pot+i, opponent_pot*9:(opponent_pot+1)*9]) == 1:
        home_opponents.append(np.argmax(graph[9*pot+i, opponent_pot*9:(opponent_pot+1)*9])%9)
    else:
        for j in range(9):
            if (pot, i) != (opponent_pot, j) and np.sum(graph[9*pot:9*(pot+1), 9*opponent_pot+j]) == 0 and graph[9*opponent_pot+j, 9*pot+i] == 0:
                home_opponents.append(j)
    away_opponents = []
    if np.sum(graph[9*opponent_pot:9*(opponent_pot+1), 9*pot+i]) == 1:
        away_opponents.append(np.argmax(graph[9*opponent_pot:9*(opponent_pot+1), 9*pot+i])%9)
    else:
        for j in range(9):
            if (pot, i) != (opponent_pot, j) and np.sum(graph[9*opponent_pot+j, 9*pot:9*(pot+1)]) == 0 and graph[9*pot+i, 9*opponent_pot+j] == 0:
                away_opponents.append(j)
    all_opponents = [(x, y) for x in home_opponents for y in away_opponents if x != y]
    feasible_opponents = []
    for (home, away) in all_opponents:
        copy_graph = np.copy(graph)
        copy_graph[9*pot+i, 9*opponent_pot+home] = 1
        copy_graph[9*opponent_pot+away, 9*pot+i] = 1
        if is_feasible(copy_graph, pot+(i+opponent_pot==11), (i+(opponent_pot==3))%9, (opponent_pot+1)%4):
            feasible_opponents.append((home, away))
    return feasible_opponents

    
def is_feasible(graph, pot, i, opponent_pot):
    if pot == 4:
        return True
    else:
        if np.sum(graph[9*pot+i, 9*opponent_pot:9*(opponent_pot+1)]) == 1:
            return is_feasible(graph, pot+(i+opponent_pot==11), (i+(opponent_pot==3))%9, (opponent_pot+1)%4)
        else:
            for j in range(9): 
                if (pot, i) != (opponent_pot, j) and np.sum(graph[9*pot:9*(pot+1), 9*opponent_pot+j]) == 0 and graph[9*opponent_pot+j, 9*pot+i] == 0: # on peut placer un 1
                    graph[9*pot+i, 9*opponent_pot+j] = 1
                    if is_feasible(graph, pot+(i+opponent_pot==11), (i+(opponent_pot==3))%9, (opponent_pot+1)%4):
                        return True
                    else:
                        graph[9*pot+i,9*opponent_pot+j] = 0
            return False


def tirage_au_sort(graph):
    for pot in range(4):
        for i in range(9):
            opponents = []
            for opponent_pot in range(4):
                (home, away) = random.choice(possible_opponents(graph, pot, i, opponent_pot))
                graph[9*pot+i, 9*opponent_pot+home] = 1
                graph[9*opponent_pot+away, 9*pot+i] = 1
                opponents.append((home, away))
            print("Opponents of team {} from pot {}: {}".format(i, pot, opponents))


graph = np.zeros((36, 36))
tirage_au_sort(graph)