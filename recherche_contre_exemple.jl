using JuMP, Gurobi

using JuMP, Gurobi

function find_regular_graph()
    # Créer le modèle avec Gurobi comme solveur
    model = Model(Gurobi.Optimizer)

    # Paramètres
    N = 36
    group_size = 9
    groupes = [1:9, 10:18, 19:27, 28:36] # Les indices en Julia sont corrects
    groupe_biparti_1 = [1,2,10,11,19,20,28,29]
    groupe_biparti_2 = [3,4,12,13,21,22,30,31]
    nb_color = 8

    # Variables
    @variable(model, x[1:N, 1:N, 1:nb_color], Bin)

    # Contraintes d'unicité de couleur pour les arêtes partant d'un même sommet
    for i in 1:N
        for c in 1:nb_color
            @constraint(model, sum(x[i, j, c] for j in 1:N if j != i) <= 1)
        end
    end

    # On ne peut pas colorier une arête avec deux couleurs différentes
    for i in 1:N, j in 1:N
        if i != j
            @constraint(model, sum(x[i, j, c] for c in 1:nb_color) <= 1)
        end
    end

    # Deux arêtes par sommet dans chaque groupe
    for i in 1:N
        for group in groupes
            @constraint(model, sum(x[i, j, c] for j in group for c in 1:nb_color if i != j) == 2)
        end
    end

    # Éviter les boucles et assurer la symétrie des arêtes
    for i in 1:N, c in 1:nb_color
        @constraint(model, x[i, i, c] == 0)
        for j in 1:N
            @constraint(model, x[i, j, c] == x[j, i, c])
        end
    end

     # Contraintes pour imposer un graphe complet (8-8) régulier bipartite
    for i in groupe_biparti_1, j in groupe_biparti_2
        @constraint(model, sum(x[i, j, c] for c in 1:nb_color) == 1)
    end




    # Résolution du modèle
    optimize!(model)
    if termination_status(model) == MOI.OPTIMAL
        println("Une solution existe.")
        aretes = []
        for i in 1:N
            for j in i+1:N
                for c in 1:nb_color
                    if value(x[i, j, c]) > 0.5
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
