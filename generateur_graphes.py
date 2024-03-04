import random

graph = [[0] * 36 for _ in range(36)]


def count_opponents(current_pot, current_i, other_pot):
    return sum(graph[current_pot*9 + current_i][other_pot*9:(other_pot+1)*9])


def all_possible_couple_opponents(current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(9):
        if count_opponents(opponent_pot, opponent_i, current_pot) < 2 and opponent_i != current_i:
            for opponent_j in range(opponent_i+1, 9):
                if count_opponents(opponent_pot, opponent_j, current_pot) < 2 and opponent_j != current_i:
                    graph[current_pot*9 + current_i][opponent_pot*9 + opponent_i] = 1
                    graph[opponent_pot*9 + opponent_i][current_pot*9 + current_i] = 1
                    graph[current_pot*9 + current_i][opponent_pot*9 + opponent_j] = 1
                    graph[opponent_pot*9 + opponent_j][current_pot*9 + current_i] = 1
                    if fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9),
                                  (current_i + (opponent_pot == 3)) % 9,
                                  (opponent_pot + 1) % 4):
                        possible_opponents.append((opponent_i, opponent_j))
                    graph[current_pot*9 + current_i][opponent_pot*9 + opponent_i] = 0
                    graph[opponent_pot*9 + opponent_i][current_pot*9 + current_i] = 0
                    graph[current_pot*9 + current_i][opponent_pot*9 + opponent_j] = 0
                    graph[opponent_pot*9 + opponent_j][current_pot*9 + current_i] = 0
    return possible_opponents


def all_possible_opponents(current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(9):
        if count_opponents(opponent_pot, opponent_i, current_pot) < 2 and opponent_i != current_i:
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_i] = 1
            graph[opponent_pot*9 + opponent_i][current_pot*9 + current_i] = 1
            if fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9),
                          (current_i + (opponent_pot == 3)) % 9,
                          (opponent_pot + 1) % 4):
                possible_opponents.append(opponent_i)
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_i] = 0
            graph[opponent_pot*9 + opponent_i][current_pot*9 + current_i] = 0
    return possible_opponents


def fill_graph(current_pot, current_i, opponent_pot):
    if current_pot == 4:  # no more team to place
        print("It completed totally the graph")
        return True
    else:
        print(current_pot, current_i, opponent_pot)
        if count_opponents(current_pot, current_i, opponent_pot) == 0:
            all_possibilities = all_possible_couple_opponents(current_pot, current_i, opponent_pot)
            if all_possibilities == []:
                return False
            else:
                opponents = random.choice(all_possibilities)
                opponent_1, opponent_2 = opponents
                graph[current_pot*9 + current_i][opponent_pot*9 + opponent_1] = 1
                graph[opponent_pot*9 + opponent_1][current_pot*9 + current_i] = 1
                graph[current_pot*9 + current_i][opponent_pot*9 + opponent_2] = 1
                graph[opponent_pot*9 + opponent_2][current_pot*9 + current_i] = 1
                fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9),
                          (current_i + (opponent_pot == 3)) % 9,
                          (opponent_pot + 1) % 4)
        elif count_opponents(current_pot, current_i, opponent_pot) == 1:
            all_possibilities = all_possible_opponents(current_pot, current_i, opponent_pot)
            if all_possibilities == []:
                return False
            else:
                opponent = random.choice(all_possibilities)
                graph[current_pot*9 + current_i][opponent_pot*9 + opponent] = 1
                graph[opponent_pot*9 + opponent][current_pot*9 + current_i] = 1
                fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9),
                          (current_i + (opponent_pot == 3)) % 9,
                          (opponent_pot + 1) % 4)
        elif count_opponents(current_pot, current_i, opponent_pot) > 2:
            return False


fill_graph(0, 0, 0)
print(graph)
