import random

# Non remplir itérativement juste en regardant la disponibilité des équipes ne garantit pas la convergence de la solution

def count_opponents(graph, current_pot, current_i, other_pot):
    return sum(graph[current_pot*9 + current_i][other_pot*9:(other_pot+1)*9])


def all_possible_opponents(graph, current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(9):
        if count_opponents(graph, opponent_pot, opponent_i, current_pot) < 2 and (current_pot, current_i) != (opponent_pot, opponent_i):
            possible_opponents.append(opponent_i)
    return possible_opponents


def fill_graph(graph, current_pot, current_i, opponent_pot):
    if current_pot == 4:  # no more team to place
        return graph
    else:
        possible_opponents = all_possible_opponents(graph, current_pot, current_i, opponent_pot)
        number_opponents = count_opponents(graph, current_pot, current_i, opponent_pot)
        if number_opponents == 0:              
            opponent_1, opponent_2 = random.sample(possible_opponents, 2)
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_1] = 1
            graph[opponent_pot*9 + opponent_1][current_pot*9 + current_i] = 1
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_2] = 1
            graph[opponent_pot*9 + opponent_2][current_pot*9 + current_i] = 1
        elif number_opponents == 1:
            opponent = random.choice(possible_opponents)
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent] = 1
            graph[opponent_pot*9 + opponent][current_pot*9 + current_i] = 1
        opponent_pot = (opponent_pot + 1) % 4
        current_i = (current_i + (opponent_pot == 0)) % 9
        current_pot = current_pot + (current_i + opponent_pot == 0)
        fill_graph(graph, current_pot, current_i, opponent_pot)


fill_graph([[0] * 36 for _ in range(36)], 0, 0, 0)