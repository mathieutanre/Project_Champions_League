using LightGraphs
using Random

function create_initial_graph()
    G = SimpleGraph(36)
    # Ajoute une sous-clique et des arêtes spécifiques
    for i in 1:8
        for j in (i+1):8
            add_edge!(G, i, j)
        end
    end
    add_edge!(G, 9, 1)
    add_edge!(G, 9, 2)
    add_edge!(G, 9, 3)
    add_edge!(G, 9, 4)
    add_edge!(G, 9, 5)
    add_edge!(G, 9, 6)
    add_edge!(G, 9, 7)
    return G
end

function find_pair(G, target_degree)
    n = nv(G)
    vertices = shuffle(1:n)
    for v1 in vertices
        if degree(G, v1) < target_degree
            for v2 in shuffle(vertices)
                if v1 != v2 && !has_edge(G, v1, v2) && degree(G, v2) < target_degree
                    return v1, v2
                end
            end
        end
    end
    return 0, 0 # Indique une impasse
end

function complete_to_regular_graph(target_degree)
    while true
        G = create_initial_graph()
        stuck = false
        while true
            if all(deg -> deg == target_degree, degree(G))
                return G
            end
            v1, v2 = find_pair(G, target_degree)
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

# Essayez de compléter le graphe jusqu'à ce qu'un graphe valide soit trouvé
G_final = complete_to_regular_graph(8)
println("Un graphe 8-régulier satisfaisant les conditions a été trouvé.")

println("Degrés des sommets après tentative de complétion : ", degree(G_final))

function is_8_coloriable(G)
    n_edges = LightGraphs.ne(G)
    edges = collect(LightGraphs.edges(G))
    n_vertices = LightGraphs.nv(G)
    
    # Pour un graphe 8-régulier, testons directement avec 8 couleurs
    max_colors = 8
    
    model = Model(Gurobi.Optimizer)
    set_optimizer_attribute(model, "OutputFlag", 0)
    
    @variable(model, x[1:n_edges, 1:max_colors], Bin)
    
    # Chaque arête reçoit au moins une couleur
    @constraint(model, [e in 1:n_edges], sum(x[e, :]) == 1)
    
    # Deux arêtes incidentes ne peuvent pas partager la même couleur
    for v in 1:n_vertices
        adj_edges = [i for (i, e) in enumerate(edges) if v in e.src || v in e.dst]
        for c in 1:max_colors
            @constraint(model, sum(x[e, c] for e in adj_edges) <= 1)
        end
    end
    
    optimize!(model)
    
    return termination_status(model) == MOI.OPTIMAL
end

println("Degrés des sommets après tentative de complétion : ", is_8_coloriable(G_final))
