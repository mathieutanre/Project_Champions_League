using JuMP, Gurobi

function find_regular_graph()
    # Créer le modèle avec Gurobi comme solveur
    model = Model(Gurobi.Optimizer)

    # Nombre total de sommets (4 groupes de 9 sommets chacun)
    N = 36
    # Nombre de sommets par groupe
    group_size = 9
    groupes = [0:8, 9:17, 18:26, 27:35]
    # Sommets formant une clique
    clique = [0, 1, 9, 10, 18, 19, 27, 28]

    # Variable binaire pour les arêtes, 1 si une arête existe entre i et j, 0 sinon
    @variable(model, x[0:N-1, 0:N-1], Bin)


    # Chaque sommet est relié à exactement deux sommets dans chaque groupe
    for i in 0:N-1
        for pot_start in 0:9:27
            @constraint(model, sum(x[i, j] for j in pot_start:pot_start+8) == 2)
        end
    end

    # Éviter les arêtes doubles et les boucles Graphe non orienté
    for i in 0:N-1
        @constraint(model, x[i, i] == 0)
        for j in 0:N-1
            @constraint(model, x[i, j] == x[j, i])
        end
    end

    # Chaque équipe de la clique doit être relié
    for i in 1:7
        for j in i+1:7
            @constraint(model, x[clique[i], clique[j]] == 1)
        end
    end

    @constraint(model, x[0, 2] == 1)
    @constraint(model, x[1, 2] == 1)
    
    

    #--------------------------------------- SOLVEUR ---------------------------------------------------------------------

    # Résolution du modèle
    optimize!(model)
    if termination_status(model) == MOI.OPTIMAL
        println("Une solution existe.")
        aretes = []
        for i in 0:N-1
            for j in i+1:N-1  # Utiliser i+1 pour éviter les doublons
                if value(x[i, j]) > 0.5  # Si x[i, j] est arrondi à 1
                    push!(aretes, (i, j))
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
