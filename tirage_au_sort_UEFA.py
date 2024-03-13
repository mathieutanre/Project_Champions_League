import random
import numpy as np

# rajouter fonction all_possible pour éliminer et pas parcourir tous les j puis la fonction de tirage

def is_feasible(graph, pot, i, opponent_pot):
    if pot == 4:
        return True
    for j in range(9): 
        if (pot, i) != (opponent_pot, j) and np.sum(graph[pot*9:(pot+1)*9, j]) == 0: # on peut placer un 1
            graph[9 * pot + i, 9 * opponent_pot + j] = 1
            if is_feasible(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9,  (opponent_pot + 1) % 4):
                return True
            graph[9 * pot + i, 9 * opponent_pot + j] = 0
    return False

graph = np.zeros((36, 36))
print(is_feasible(graph, 0, 0, 0))
print(graph)
        
                

        