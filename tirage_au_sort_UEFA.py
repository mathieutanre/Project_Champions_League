import random
import numpy as np


def is_fillable(graph, pot, opponent_pot): # checks if the quadrant (pot, opponent_pot) can be filled
    def aux(graph, i):
        if i==9:
            return True
        else:
            home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != -1]
            away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != -1]
            possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
            for (home, away) in possible_matches:
                new_graph = np.copy(graph)
                new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
                new_graph[9*opponent_pot+home, 9*pot+i] = -1
                for k in range(9):
                    if k != home:
                        new_graph[9*pot+i, 9*opponent_pot+k] = -1
                    if k != i:
                        new_graph[9*pot+k, 9*opponent_pot+home] = -1
                new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
                new_graph[9*pot+i, 9*opponent_pot+away] = -1
                for k in range(9):
                    if k != away:
                        new_graph[9*opponent_pot+k, 9*pot+i] = -1
                    if k != i:
                        new_graph[9*opponent_pot+away, 9*pot+k] = -1
                if aux(graph, i+1):
                    return True
            return False
    return aux(graph, 0)
        

def all_matches(graph, pot, i, opponent_pot): # returns all the matches possible between the team (pot, i) with the opponent_pot
    home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != -1]
    away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != -1]
    possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
    true_matches = []
    for (home, away) in possible_matches:
        new_graph = np.copy(graph)
        new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
        new_graph[9*opponent_pot+home, 9*pot+i] = -1
        for k in range(9):
            if k != home:
                new_graph[9*pot+i, 9*opponent_pot+k] = -1
            if k != i:
                new_graph[9*pot+k, 9*opponent_pot+home] = -1
        new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
        new_graph[9*pot+i, 9*opponent_pot+away] = -1
        for k in range(9):
            if k != away:
                new_graph[9*opponent_pot+k, 9*pot+i] = -1
            if k != i:
                new_graph[9*opponent_pot+away, 9*pot+k] = -1
        if is_fillable(new_graph, pot, opponent_pot) and is_fillable(new_graph, opponent_pot, pot):
            true_matches.append((home, away))
    return true_matches
    

def tirage_au_sort(graph):
    for pot in range(4):
        for i in range(9):
            opponents = []
            for opponent_pot in range(4):
                (home, away) = random.choice(all_matches(graph, pot, i, opponent_pot))
                graph[9*pot+i, 9*opponent_pot+home] = 1
                graph[9*opponent_pot+home, 9*pot+i] = -1
                for k in range(9):
                    if k != home:
                        graph[9*pot+i, 9*opponent_pot+k] = -1
                    if k != i:
                        graph[9*pot+k, 9*opponent_pot+home] = -1
                graph[9*opponent_pot+away, 9*pot+i] = 1
                graph[9*pot+i, 9*opponent_pot+away] = -1
                for k in range(9):
                    if k != away:
                        graph[9*opponent_pot+k, 9*pot+i] = -1
                    if k != i:
                        graph[9*opponent_pot+away, 9*pot+k] = -1
                opponents.append((home, away))
            print("Opponents for the team {}{}".format(chr(ord('A') + pot), i), opponents)

graph = np.zeros((36, 36))
np.fill_diagonal(graph, -1)
tirage_au_sort(graph)
