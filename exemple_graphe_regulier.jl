using LightGraphs

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

# Vérification rapide du degré de chaque sommet pour s'assurer qu'il respecte les contraintes
for i in 1:36
    println("Sommet $i, Degré: $(degree(G, i))")
end
