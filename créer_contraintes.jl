using JuMP, Gurobi
using Random

# Initialisation du générateur de nombres aléatoires
rng = MersenneTwister()

N = 36
max_iterations = 10000
T = 8  # Nombre de jours (couleurs)

for iteration in 1:max_iterations
    model = Model(Gurobi.Optimizer)
    set_optimizer_attribute(model, "OutputFlag", 0)  # Désactiver les logs pour la lisibilité
    
    @variable(model, x[1:N, 1:N], Bin)
    
    @constraint(model, no_self_play[i in 1:N], x[i, i] == 0)

    @constraint(model, max_one_game[i in 1:N, j in 1:N; i != j], x[i, j] + x[j, i] <= 1)

    for i in 1:N
        for pot_start in 1:9:28
            @constraint(model, sum(x[i, j] for j in pot_start:pot_start+8) == 1)
            @constraint(model, sum(x[j, i] for j in pot_start:pot_start+8) == 1)
        end
    end

    @objective(model, Max, sum(rand(rng) * x[i, j] for i in 1:N, j in 1:N))
    
    optimize!(model)

    for i in 1:N
        for j in 1:N
            # Vérifie si x[i, j] est égal à 1 dans la solution
            if value(x[i, j]) > 0.5  # Utilisez une petite marge pour les problèmes de précision flottante
                println("L'équipe $i joue contre l'équipe $j")
            end
        end
    end
    
    # Extraction des matchs
    matches = [(i, j) for i in 1:N, j in 1:N if value(x[i, j]) > 0.5]
    
    # Création du modèle pour tester la colorabilité
    color_model = Model(Gurobi.Optimizer)
    set_optimizer_attribute(color_model, "OutputFlag", 0)
    
    @variable(color_model, y[1:N, 1:N, 1:T], Bin)
    
    # Chaque match joué exactement un jour
    @constraint(color_model, match_played_once[i in 1:N, j in 1:N; (i, j) in matches], sum(y[i, j, t] for t in 1:T) == 1)

    # Chaque équipe joue une fois par jour
    @constraint(color_model, team_plays_once_per_day[t in 1:T, i in 1:N], sum(y[i, j, t] + y[j, i, t] for j in 1:N) == 1)

    optimize!(color_model)
    
    # Vérifie si le graphe est 8-coloriable
    if termination_status(color_model) != MOI.OPTIMAL
        println("Le graphe n'est pas 8-coloriable à l'itération $iteration.")
        for i in 1:N
            for j in 1:N
                # Vérifie si x[i, j] est égal à 1 dans la solution
                if value(x[i, j]) > 0.5  # Utilisez une petite marge pour les problèmes de précision flottante
                    println("L'équipe $i joue contre l'équipe $j")
                end
            end
        end
        break  # Sort de la boucle si un graphe non 8-coloriable est trouvé
    end

    println("Le graphe est 8-coloriable à l'itération $iteration.")

end



