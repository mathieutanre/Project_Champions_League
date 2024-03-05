import random


def count_opponents(graph, current_pot, current_i, other_pot):
    return sum(graph[current_pot*9 + current_i][other_pot*9:(other_pot+1)*9])


def all_possible_opponents(graph, current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(9):
        if count_opponents(graph, opponent_pot, opponent_i, current_pot) < 2 and opponent_i != current_i:
            possible_opponents.append(opponent_i)
    return possible_opponents


def fill_graph(graph, current_pot, current_i, opponent_pot):
    if current_pot == 4:  # no more team to place
        return graph
    else:
        print(graph)
        possible_opponents = all_possible_opponents(graph, current_pot, current_i, opponent_pot)
        number_opponents = count_opponents(graph, current_pot, current_i, opponent_pot)
        if number_opponents == 0:              
            opponent_1, opponent_2 = random.sample(possible_opponents, 2)
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_1] = 1
            graph[opponent_pot*9 + opponent_1][current_pot*9 + current_i] = 1
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_2] = 1
            graph[opponent_pot*9 + opponent_2][current_pot*9 + current_i] = 1
        if number_opponents == 1:
            opponent = random.choice(possible_opponents)
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent] = 1
            graph[opponent_pot*9 + opponent][current_pot*9 + current_i] = 1
        fill_graph(graph,
                  current_pot + (current_i + (opponent_pot == 3) == 9),
                  (current_i + (opponent_pot == 3)) % 9,
                  (opponent_pot + 1) % 4)


fill_graph([[0] * 36 for _ in range(36)], 0, 0, 0)