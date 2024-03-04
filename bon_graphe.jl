using LightGraphs
using Random

# Crée un graphe vide avec les conditions initiales spécifiques
function create_initial_graph()
    return SimpleGraph(36)
end

# Initialisation du graphe
G = SimpleGraph(36)

# Fonction pour ajouter des arêtes en respectant les contraintes (2,2,2,2)-régulières
function add_edges_respecting_constraints!(G)
    # Première tranche de 9 sommets
    for i in 1:9
        # Connecte chaque sommet à 2 sommets dans chaque tranche suivante
        add_edge!(G, i, ((i % 9) + 1) + 9) # Groupe 2
        add_edge!(G, i, ((i + 1) % 9) + 9) # Groupe 2
        add_edge!(G, i, ((i % 9) + 1) + 18) # Groupe 3
        add_edge!(G, i, ((i + 1) % 9) + 18) # Groupe 3
        add_edge!(G, i, ((i % 9) + 1) + 27) # Groupe 4
        add_edge!(G, i, ((i + 1) % 9) + 27) # Groupe 4
    end

    # Pour les sommets 10-36, les arêtes ont déjà été ajoutées par les boucles précédentes
    # Puisque chaque sommet dans les groupes 2, 3, et 4 est connecté à deux sommets dans le groupe 1
    # et les connexions entre les groupes 2, 3, et 4 sont déjà faites symétriquement.
end

# Ajoute les arêtes en respectant les contraintes spécifiques
add_edges_respecting_constraints!(G)


# Trouve une paire de sommets valide qui respecte les contraintes (2,2,2,2)-régulières
function find_valid_pair(G)
    n = nv(G)
    for _ in 1:10000 # Augmente le nombre d'essais pour éviter une boucle infinie
        v1 = rand(1:n)
        group_v1 = get_group(v1)
        # Sélectionne un sommet dans le même groupe que v1 pour vérifier la connexion
        v2 = rand((group_v1-1)*9+1:group_v1*9)
        if v1 != v2 && !has_edge(G, v1, v2) && is_valid_edge(G, v1, v2)
            return v1, v2
        end
    end
    return 0, 0 # Retourne une paire nulle si aucune paire valide n'est trouvée
end

# Détermine à quel groupe de 9 sommets appartient un sommet donné
function get_group(vertex)
    return ceil(Int, vertex / 9)
end

# Vérifie si une arête peut être ajoutée sans violer les contraintes (2,2,2,2)-régulières
function is_valid_edge(G, v1, v2)
    group_v1 = get_group(v1)
    group_v2 = get_group(v2)
    # Vérifie si les sommets v1 et v2 ne dépassent pas 2 connexions dans leur groupe respectif
    for group in 1:4
        vertices_in_group = ((group-1)*9+1):group*9
        if sum([has_edge(G, v1, v) for v in vertices_in_group]) >= 2 || sum([has_edge(G, v2, v) for v in vertices_in_group]) >= 2
            return false
        end
    end
    return true
end

function complete_to_regular_graph(G)
    while true
        #G = create_initial_graph()
        stuck = false
        while true
            if all(v -> all(group -> sum([has_edge(G, v, u) for u in ((group-1)*9+1):group*9]) == 2, 1:4), 1:nv(G))
                return G
            end
            v1, v2 = find_valid_pair(G)
            if v1 == 0 && v2 == 0
                stuck = true
                break
            end
            add_edge!(G, v1, v2)
        end
        if !stuck
            break
        end
    end
end

# Essaye de compléter le graphe jusqu'à ce qu'un graphe valide soit trouvé
G_final = complete_to_regular_graph(G)
println("Un graphe (2,2,2,2)-régulier a été trouvé.")
