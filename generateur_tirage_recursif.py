import random


graph = [[0] * 36 for _ in range(36)]


def count_opponents(current_pot, current_i, other_pot):
    return sum(graph[current_pot*9 + current_i][other_pot*9:(other_pot+1)*9])


def random_opponents(current_pot, current_i, opponent_pot, nb_opponents):
    possible_opponents = []
    for opponent_i in range(9):
        if (current_pot, current_i) != (opponent_pot, opponent_i):
            if count_opponents(opponent_pot, opponent_i, current_pot) < 2:
                if fill_graph((opponent_pot + 1) % 4, (current_i + (opponent_pot == 0)) % 9, current_pot + (current_i + opponent_pot == 0)):
                    possible_opponents.append(opponent_i)
    if nb_opponents == 0:
        return random.sample(possible_opponents, 2)
    elif nb_opponents == 1:
        return random.choice(possible_opponents)


def fill_graph(current_pot, current_i, opponent_pot):
    if current_pot == 4:  # no more team to place
        print("Done")
        return True
    else:
        nb_opponents = count_opponents(current_pot, current_i, opponent_pot)
        opponent = random_opponents(current_pot, current_i, opponent_pot, nb_opponents) 
        if nb_opponents == 0:  
            opponent_1, opponent_2 = opponent[0], opponent[1]           
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_1] = 1
            graph[opponent_pot*9 + opponent_1][current_pot*9 + current_i] = 1
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent_2] = 1
            graph[opponent_pot*9 + opponent_2][current_pot*9 + current_i] = 1
        elif nb_opponents == 1:
            graph[current_pot*9 + current_i][opponent_pot*9 + opponent] = 1
            graph[opponent_pot*9 + opponent][current_pot*9 + current_i] = 1
        opponent_pot = (opponent_pot + 1) % 4
        current_i = (current_i + (opponent_pot == 0)) % 9
        current_pot = current_pot + (current_i + opponent_pot == 0)
        fill_graph(current_pot, current_i, opponent_pot)


fill_graph(0, 0, 0)
print(graph)