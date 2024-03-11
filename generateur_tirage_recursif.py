import random

# Je regarde la liste des éléments a priori admissibles et je vérifie parmi eux dans le désordre si elle est admissible (avec une autre fonction)


def count_opponents(graph, pot, i, other_pot):
    return sum(graph[pot*9 + i][other_pot*9:(other_pot+1)*9])


def possible_opponents(graph, pot, i, opponent_pot, nb_opponents):
    opponents = []
    for opponent_i in range(9):
        if (pot, i) != (opponent_pot, opponent_i) and count_opponents(graph, opponent_pot, opponent_i, pot) < 2:
            opponents.append(opponent_i)
    if nb_opponents >= 2:
        return []
    elif nb_opponents == 1:
        return opponents
    elif nb_opponents == 0:
        return [(opponents[i], opponents[j]) for i in range(len(opponents)) for j in range(i+1, len(opponents))]
    

def fill_graph(graph, pot, i, opponent_pot):
    if pot == 4: # no more team to place
        print(graph)
        return True
    else:
        print(pot, i, opponent_pot)
        nb_opponents = count_opponents(graph, pot, i, opponent_pot)
        if nb_opponents > 2:
            return False
        elif nb_opponents == 2:
            return fill_graph(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9, (opponent_pot + 1) % 4)
        elif nb_opponents == 1:
            opponents = []
            for opponent_i in possible_opponents(graph, pot, i, opponent_pot, nb_opponents):
                graph[pot*9 + i][opponent_pot*9 + opponent_i] = 1
                graph[opponent_pot*9 + opponent_i][pot*9 + i] = 1
                if fill_graph(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9, (opponent_pot + 1) % 4):
                    opponents.append(opponent_i)
                graph[pot*9 + i][opponent_pot*9 + opponent_i] = 0
                graph[opponent_pot*9 + opponent_i][pot*9 + i] = 0
            if len(opponents) == 0:
                return False
            else:
                random_opponent_i = random.choice(opponents)
                graph[pot*9 + i][opponent_pot*9 + random_opponent_i] = 1
                graph[opponent_pot*9 + random_opponent_i][pot*9 + i] = 1
                return fill_graph(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9, (opponent_pot + 1) % 4)
        elif nb_opponents == 0: 
            opponents = []
            for (opponent_i, opponent_j) in possible_opponents(graph, pot, i, opponent_pot, nb_opponents):
                graph[pot*9 + i][opponent_pot*9 + opponent_i] = 1
                graph[opponent_pot*9 + opponent_i][pot*9 + i] = 1
                graph[pot*9 + i][opponent_pot*9 + opponent_j] = 1
                graph[opponent_pot*9 + opponent_j][pot*9 + i] = 1
                if fill_graph(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9, (opponent_pot + 1) % 4):
                    opponents.append((opponent_i, opponent_j))
                graph[pot*9 + i][opponent_pot*9 + opponent_i] = 0
                graph[opponent_pot*9 + opponent_i][pot*9 + i] = 0
                graph[pot*9 + i][opponent_pot*9 + opponent_j] = 0
                graph[opponent_pot*9 + opponent_j][pot*9 + i] = 0
            if len(opponents) == 0:
                return False
            else:
                (random_opponent_i, random_opponent_j) = random.choice(opponents)
                graph[pot*9 + i][opponent_pot*9 + random_opponent_i] = 1
                graph[opponent_pot*9 + random_opponent_i][pot*9 + i] = 1
                graph[pot*9 + i][opponent_pot*9 + random_opponent_j] = 1
                graph[opponent_pot*9 + random_opponent_j][pot*9 + i] = 1
                return fill_graph(graph, pot + (i + opponent_pot == 11), (i + (opponent_pot == 3)) % 9, (opponent_pot + 1) % 4)

fill_graph([[0] * 36 for _ in range(36)], 0, 0, 0)