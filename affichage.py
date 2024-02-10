import networkx as nx
import matplotlib.pyplot as plt

# Données complètes des rencontres
rencontres = [
    (1, "A1", "B1"), (1, "A3", "D7"), (1, "A5", "B4"), (1, "A7", "D2"), (1, "A8", "A9"),
    (1, "B3", "D9"), (1, "B5", "C4"), (1, "B7", "B8"), (1, "B9", "C9"), (1, "C1", "C2"),
    (1, "C3", "A2"), (1, "C5", "A4"), (1, "C7", "B6"), (1, "C8", "D6"), (1, "D1", "B2"),
    (1, "D3", "D4"), (1, "D5", "C6"), (1, "D8", "A6"), (2, "A2", "B5"), (2, "A4", "C3"),
    (2, "A6", "A7"), (2, "A9", "A1"), (2, "B1", "C8"), (2, "B2", "B3"), (2, "B4", "D5"),
    (2, "B6", "D1"), (2, "B8", "A3"), (2, "C2", "A5"), (2, "C4", "B9"), (2, "C6", "C7"),
    (2, "C9", "C1"), (2, "D2", "D3"), (2, "D4", "B7"), (2, "D6", "C5"), (2, "D7", "D8"),
    (2, "D9", "A8"), (3, "A1", "D4"), (3, "A3", "A4"), (3, "A5", "C6"), (3, "A7", "C2"),
    (3, "A8", "B6"), (3, "B3", "A2"), (3, "B5", "D6"), (3, "B7", "D2"), (3, "B9", "B1"),
    (3, "C1", "B2"), (3, "C3", "C4"), (3, "C5", "B4"), (3, "C8", "A6"), (3, "D1", "C9"),
    (3, "D3", "B8"), (3, "D5", "A9"), (3, "D7", "C7"), (3, "D8", "D9"), (4, "A2", "C1"),
    (4, "A4", "A5"), (4, "A6", "B9"), (4, "A9", "D8"), (4, "B1", "D3"), (4, "B2", "A7"),
    (4, "B4", "B5"), (4, "B6", "B7"), (4, "B8", "D7"), (4, "C2", "D1"), (4, "C4", "C5"),
    (4, "C6", "A1"), (4, "C7", "A8"), (4, "C9", "B3"), (4, "D2", "C3"), (4, "D4", "D5"),
    (4, "D6", "A3"), (4, "D9", "C8"), (5, "A1", "C4"), (5, "A3", "B2"), (5, "A5", "A6"),
    (5, "A7", "B8"), (5, "A8", "D6"), (5, "B3", "C6"), (5, "B5", "B6"), (5, "B7", "C7"),
    (5, "B9", "A4"), (5, "C1", "A9"), (5, "C3", "D4"), (5, "C5", "D9"), (5, "C8", "C9"),
    (5, "D1", "D2"), (5, "D3", "A2"), (5, "D5", "B1"), (5, "D7", "B4"), (5, "D8", "C2"),
    (6, "A2", "A3"), (6, "A4", "D5"), (6, "A6", "C5"), (6, "A9", "B7"), (6, "B1", "A5"),
    (6, "B2", "D8"), (6, "B4", "A8"), (6, "B6", "C3"), (6, "B8", "B9"), (6, "C2", "B5"),
    (6, "C4", "A7"), (6, "C6", "D7"), (6, "C7", "C8"), (6, "C9", "D3"), (6, "D2", "A1"),
    (6, "D4", "C1"), (6, "D6", "B3"), (6, "D9", "D1"), (7, "A1", "A2"), (7, "A3", "C7"),
    (7, "A5", "D9"), (7, "A8", "C9"), (7, "B2", "C2"), (7, "B3", "B4"), (7, "B5", "A9"),
    (7, "B7", "A6"), (7, "B9", "D4"), (7, "C1", "D2"), (7, "C3", "B1"), (7, "C5", "C6"),
    (7, "C8", "B8"), (7, "D1", "A7"), (7, "D3", "C4"), (7, "D5", "D6"), (7, "D7", "A4"),
    (7, "D8", "B6"), (8, "A2", "D1"), (8, "A4", "B3"), (8, "A6", "D3"), (8, "A7", "A8"),
    (8, "A9", "C8"), (8, "B1", "B2"), (8, "B4", "C1"), (8, "B6", "A1"), (8, "B8", "C5"),
    (8, "C2", "C3"), (8, "C4", "D5"), (8, "C6", "B7"), (8, "C7", "D8"), (8, "C9", "A3"),
    (8, "D2", "B5"), (8, "D4", "A5"), (8, "D6", "D7"), (8, "D9", "B9"),
]




def rencontres_inter_pots(char1, char2, rencontres):
    li_rencontres_inter_pots = []
    for rencontre in rencontres:
        if (str(char1) in rencontre[1] and str(char2) in rencontre[2]) or (str(char2) in rencontre[1] and str(char1) in rencontre[2]):
            li_rencontres_inter_pots.append(rencontre)
    return li_rencontres_inter_pots

rencontres_AC = rencontres_inter_pots("A", "C", rencontres)
rencontres_AB = rencontres_inter_pots("A", "B", rencontres)
rencontres_AD = rencontres_inter_pots("A", "D", rencontres)
rencontres_BC = rencontres_inter_pots("B", "C", rencontres)
rencontres_BD = rencontres_inter_pots("B", "D", rencontres)

li_rencontres_interpots = [rencontres_AB, rencontres_AC, rencontres_AD, rencontres_BC, rencontres_BD]

for li_rencontres in li_rencontres_interpots:
    # Création du graphe orienté
    G = nx.DiGraph()

    # Ajout des arêtes avec le jour comme attribut
    for jour, team1, team2 in li_rencontres:
        G.add_edge(team1, team2, day=jour)

    # Définition d'un système de couleurs pour les jours
    colors = {1: 'red', 2: 'blue', 3: 'green', 4: 'yellow', 5: 'orange', 6: 'purple', 7: 'brown', 8: 'grey'}

    # Assignation des couleurs aux arêtes en fonction du jour
    edge_colors = [colors[G[u][v]['day']] for u, v in G.edges()]

    # Dessin du graphe
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, edge_color=edge_colors, node_size=2000, font_size=10, arrowsize=20)
    plt.show()
