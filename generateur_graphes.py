import random

graph = [[0] * 36 for _ in range(36)]


def count_opponent(current_pot, current_i, other_pot):
    return sum(graph[current_pot*9+current_i][other_pot*9:(other_pot+1)*9])


def all_possible_couple_opponents(current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(opponent_pot*9, (opponent_pot+1)*9):
        if count_opponent(opponent_pot, opponent_i, current_pot)<2 and opponent_i!=current_i: # can play with this pot
            possible_opponents.append(opponent_i)
    possible_couple_opponents = [(possible_opponents[i], possible_opponents[j]) for i in range(len(possible_opponents)) for j in range(i+1, len(possible_opponents))]
    return possible_couple_opponents


def all_possible_opponents(current_pot, current_i, opponent_pot):
    possible_opponents = []
    for opponent_i in range(opponent_pot*9, (opponent_pot+1)*9):
        if count_opponent(opponent_pot, opponent_i, current_pot)<2 and opponent_i!=current_i: # can play with this pot
            possible_opponents.append(opponent_i)
    return possible_opponents


def fill_graph(current_pot, current_i, opponent_pot):
    if current_pot == 4: # no more team to place
        return True
    else:
        if count_opponent(current_pot, current_i, opponent_pot)==0:
            all_possibilities = all_possible_couple_opponents(current_pot, current_i, opponent_pot)    
            for possibility in all_possibilities:
                opponent_1, opponent_2 = possibility[0], possibility[1]
                graph[current_pot*9+current_i][opponent_1] = 1
                graph[opponent_1][current_pot*9+current_i] = 1
                graph[current_pot*9+current_i][opponent_2] = 1
                graph[opponent_2][current_pot*9+current_i] = 1
                if not fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9), (current_i + (opponent_pot == 3)) % 9, (opponent_pot+1)%4):
                    all_possibilities.remove(possibility) 
                graph[current_pot*9+current_i][opponent_1] = 0
                graph[opponent_1][current_pot*9+current_i] = 0
                graph[current_pot*9+current_i][opponent_2] = 0
                graph[opponent_2][current_pot*9+current_i] = 0
            if all_possibilities == []:
                    return False
            else:
                random_possibility = random.choice(all_possibilities)
                opponent_1, opponent_2 = random_possibility[0], random_possibility[1]
                graph[current_pot*9+current_i][opponent_1] = 1
                graph[opponent_1][current_pot*9+current_i] = 1
                graph[current_pot*9+current_i][opponent_2] = 1
                graph[opponent_2][current_pot*9+current_i] = 1
        if count_opponent(current_pot, current_i, opponent_pot)==1:
            all_possibilities = all_possible_opponents(current_pot, current_i, opponent_pot)    
            for possibility in all_possibilities:
                opponent = possibility
                graph[current_pot*9+current_i][opponent] = 1
                graph[opponent][current_pot*9+current_i] = 1
                print(current_pot + (current_i + (opponent_pot == 3) == 9), (current_i + (opponent_pot == 3)) % 9)
                if not fill_graph(current_pot + (current_i + (opponent_pot == 3) == 9), (current_i + (opponent_pot == 3)) % 9, (opponent_pot + 1)%4):
                    all_possibilities.remove(possibility) 
                graph[current_pot*9+current_i][opponent] = 0
                graph[opponent][current_pot*9+current_i] = 0
            if all_possibilities == []:
                return False 
            else:
                random_possibility = random.choice(all_possibilities)
                opponent = random_possibility
                graph[current_pot*9+current_i][opponent] = 1
                graph[opponent][current_pot*9+current_i] = 1
    return False
    
fill_graph(0, 0, 0)
print(graph)
