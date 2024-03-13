import matplotlib.pyplot as plt
import networkx as nx

def display_colored_graph(edge_list):
    # Créer un graphe vide
    G = nx.Graph()

    # Définition d'un système de couleurs pour les jours
    color_map = {1: 'red', 2: 'blue', 3: 'green', 4: 'yellow', 5: 'orange', 6: 'purple', 7: 'brown', 8: 'grey', 9: 'pink'}

    # Ajouter les arêtes et les attribuer une couleur selon le dictionnaire
    for i, j, c in edge_list:
        G.add_edge(i, j, color=color_map[c])  # Utilisez `color_map[c]` pour obtenir la couleur correspondante

    # Obtenir les couleurs de chaque arête en utilisant l'attribut de couleur
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    # Dessiner le graphe
    pos = nx.kamada_kawai_layout(G)  # Utiliser spring_layout pour la position des sommets
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors, node_size=1500, font_size=12, arrowsize=20, width=2)
    
    # Afficher le graphe
    plt.show()

# Liste d'arêtes avec sommets i, j et couleur c (entier)
edges =[(1, 2, 6), (1, 4, 9), (1, 10, 3), (1, 11, 2), (1, 19, 7), (1, 20, 1), (1, 28, 5), (1, 29, 8), (2, 3, 4), (2, 11, 7), (2, 12, 5), (2, 20, 9), (2, 21, 8), (2, 29, 3), (2, 30, 1), (3, 4, 8), (3, 10, 5), (3, 12, 9), (3, 19, 1), (3, 21, 2), (3, 28, 6), (3, 30, 3), (4, 13, 6), (4, 14, 2), (4, 22, 3), (4, 23, 7), (4, 31, 1), (4, 32, 4), (5, 6, 3), (5, 9, 7), (5, 14, 5), (5, 15, 4), (5, 23, 2), (5, 24, 9), (5, 32, 6), (5, 33, 1), (6, 7, 1), (6, 13, 4), (6, 15, 9), (6, 22, 8), (6, 24, 2), (6, 31, 5), (6, 33, 6), (7, 8, 2), (7, 16, 6), (7, 17, 8), (7, 25, 9), (7, 26, 4), (7, 34, 5), (7, 35, 7), (8, 9, 6), (8, 17, 7), (8, 18, 3), (8, 26, 1), (8, 27, 4), (8, 35, 5), (8, 36, 8), (9, 16, 5), (9, 18, 2), (9, 25, 3), (9, 27, 1), (9, 34, 9), (9, 36, 4), (10, 11, 9), (10, 12, 6), (10, 19, 2), (10, 20, 8), (10, 28, 1), (10, 29, 4), (11, 12, 4), (11, 20, 3), (11, 21, 5), (11, 29, 1), (11, 30, 6), (12, 19, 3), (12, 21, 1), (12, 28, 2), (12, 30, 8), (13, 14, 9), (13, 15, 5), (13, 22, 2), (13, 23, 3), (13, 31, 7), (13, 32, 1), (14, 15, 6), (14, 23, 1), (14, 24, 3), (14, 32, 8), (14, 33, 7), (15, 22, 1), (15, 24, 7), (15, 31, 2), (15, 33, 3), (16, 17, 9), (16, 18, 8), (16, 25, 1), (16, 26, 3), (16, 34, 4), (16, 35, 2), (17, 18, 4), (17, 26, 6), (17, 27, 2), (17, 35, 3), (17, 36, 1), (18, 25, 6), (18, 27, 7), (18, 34, 1), (18, 36, 5), (19, 20, 4), (19, 21, 9), (19, 28, 8), (19, 29, 5), (20, 21, 7), (20, 29, 6), (20, 30, 5), (21, 28, 3), (21, 30, 4), (22, 23, 6), (22, 24, 4), (22, 31, 9), (22, 32, 7), (23, 24, 8), (23, 32, 5), (23, 33, 4), (24, 31, 6), (24, 33, 5), (25, 26, 7), (25, 27, 8), (25, 34, 2), (25, 35, 4), (26, 27, 5), (26, 35, 9), (26, 36, 2), (27, 34, 6), (27, 36, 3), (28, 29, 7), (28, 30, 9), (29, 30, 2), (31, 32, 3), (31, 33, 8), (32, 33, 2), (34, 35, 8), (34, 36, 7), (35, 36, 6)]
display_colored_graph(edges)