using JuMP, Gurobi

function find_regular_graph()
    # Créer le modèle avec Gurobi comme solveur
    model = Model(Gurobi.Optimizer)
    N=10
    graphe = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 4), (2, 5), (2, 6), (2, 10), (3, 5), (3, 6), (3, 8), (3, 9), (3, 10), (4, 5), (4, 6), (4, 9), (4, 10), (5, 7), (5, 10), (6, 8), (6, 9), (7, 9), (7, 10), (8, 10), (9, 10)]
    pas_graphe = [(1, 10), (2, 7), (2, 8), (2, 9), (3, 4), (3, 7), (4, 7), (4, 8), (5, 6), (5, 8), (5, 9), (6, 7), (6, 10), (7, 8), (8, 9)]
    nb_color = 8

    # Variables
    @variable(model, x[1:N, 1:N, 1:nb_color], Bin)

    # Contraintes d'unicité de couleur pour les arêtes partant d'un même sommet
    for i in 1:N
        for c in 1:nb_color
            @constraint(model, sum(x[i, j, c] for j in 1:N if j != i) <= 1)
        end
    end

    #On ne peut pas colorier une arete avec deux couleurs différentes
    @constraint(model, max_one_color[i in 1:N, j in 1:N; i != j], sum(x[i, j, c] for c in 1:nb_color) <= 1)


    #Contrainte (2-2-2-2 régulier)
    for i in 1:N
        for group in groups
            @constraint(model, sum(x[i, j, c] for j in group for c in 1:nb_color) == 2)
        end
    end
        

    # Éviter les boucles et assurer la symétrie des arêtes
    for i in 1:N, c in 1:nb_color
        @constraint(model, x[i, i, c] == 0)
        for j in 1:N
            @constraint(model, x[i, j, c] == x[j, i, c])
        end
    end

    # Contraintes pour le graphe
    for k in 1:length(graphe)
            @constraint(model, sum(x[graphe[k][1], graphe[k][2], c] for c in 1:nb_color) == 1)
    end


    for k in 1:length(pas_graphe)
            @constraint(model, sum(x[pas_graphe[k][1], pas_graphe[k][2], c] for c in 1:nb_color) == 0)
    end












    


    #--------------------------------------- SOLVEUR ---------------------------------------------------------------------

    # Résolution du modèle
    optimize!(model)
    if termination_status(model) == MOI.OPTIMAL
        println("Une solution existe.")
        aretes = []
        for i in 1:N
            for j in i+1:N
                for c in 1:nb_color  # Utiliser i+1 pour éviter les doublons
                    if value(x[i, j, c]) > 0.5  # Si x[i, j] est arrondi à 1
                        push!(aretes, (i, j, c))
                    end
                end
            end
        end
        println("Arêtes du graphe trouvé :")
        println(aretes)
    else
        println("Aucune solution trouvée.")
    end
end

find_regular_graph()
