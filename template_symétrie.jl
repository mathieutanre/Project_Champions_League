using JuMP, Gurobi, Cbc

# Création du modèle avec le solveur Cbc
model = Model(Gurobi.Optimizer)

# Nombre d'équipes et de journées
N = 36
T = 8

# Définition des variables
@variable(model, x[1:N, 1:N, 1:T], Bin)

# Variables supplémentaires pour contrôler les breaks
@variable(model, break_var[1:N, 2:6], Bin)



# Contrainte : une équipe ne peut pas jouer contre elle-même
@constraint(model, no_self_play[i in 1:N, t in 1:T], x[i, i, t] == 0)

# Contrainte : une équipe joue au plus 1 fois contre chaque autre équipe
@constraint(model, max_one_game[i in 1:N, j in 1:N; i != j], sum(x[i, j, t] + x[j, i, t] for t in 1:T) <= 1)


# Contraintes spécifiques pour chaque pot
for i in 1:N
    for pot_start in 1:9:28
        @constraint(model, sum(x[i, j, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
        @constraint(model, sum(x[j, i, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
    end
end



#Fixer les variables nulles

function fix_sequential_matches(model, pot_start, pot_end)
    # Pour chaque équipe dans le pot
    for i in pot_start:pot_end
        next_team = i+1 <= pot_end ? i+1 : pot_start
        prev_team = i-1 >= pot_start ? i-1 : pot_end
        
        for j in pot_start:pot_end
            if j != next_team
                # Imposer que l'équipe i du pot1 ne joue pas contre cette équipe j du pot2
                for t in 1:T
                    fix(x[i, j, t], 0; force = true)
                end
            end
            if j != prev_team
                # Imposer que l'équipe i du pot1 ne joue pas contre cette équipe j du pot2
                for t in 1:T
                    fix(x[j, i, t], 0; force = true)
                end
            end
        end
    end
end

# Encourager un ordre séquentiel de matchs pour chaque pot
fix_sequential_matches(model, 1, 9)   # Pot A
fix_sequential_matches(model, 10, 18) # Pot B
fix_sequential_matches(model, 19, 27) # Pot C
fix_sequential_matches(model, 28, 36) # Pot D



function fix_inter_pot_matches(model, pot1_start, pot1_end, pot2_start, pot2_end)
    N_pot2 = pot2_end - pot2_start + 1 # Nombre d'équipes dans le pot2
    # Pour chaque équipe dans le pot1
    for i in pot1_start:pot1_end
        # Calcul de l'équipe cible dans le pot2 avec ajustement cyclique
        target_team_in_pot2 = pot2_start + ((i - pot1_start + 1) % N_pot2)
    
        # Parcourir toutes les équipes du pot2 pour imposer les matchs non-cibles à 0
        for j in pot2_start:pot2_end
            if j != target_team_in_pot2
                # Imposer que l'équipe i du pot1 ne joue pas contre cette équipe j du pot2
                for t in 1:T
                    fix(x[i, j, t], 0; force = true)
                end
            end
        end
    end
end

# Pot A vers Pot B et inversement
fix_inter_pot_matches(model, 1, 9, 10, 18)
fix_inter_pot_matches(model, 10, 18, 1, 9)

# Pot A vers Pot C et inversement
fix_inter_pot_matches(model, 1, 9, 19, 27)
fix_inter_pot_matches(model, 19, 27, 1, 9)

# Pot A vers Pot D et inversement
fix_inter_pot_matches(model, 1, 9, 28, 36)
fix_inter_pot_matches(model, 28, 36, 1, 9)

# Pot B vers Pot C et inversement
fix_inter_pot_matches(model, 10, 18, 19, 27)
fix_inter_pot_matches(model, 19, 27, 10, 18)

# Pot B vers Pot D et inversement
fix_inter_pot_matches(model, 10, 18, 28, 36)
fix_inter_pot_matches(model, 28, 36, 10, 18)

# Pot C vers Pot D et inversement
fix_inter_pot_matches(model, 19, 27, 28, 36)
fix_inter_pot_matches(model, 28, 36, 19, 27)





# Contrainte : chaque équipe joue exactement un match par journée
@constraint(model, one_game_per_day[t in 1:T, i in 1:N], sum(x[i, j, t] + x[j, i, t] for j in 1:N) == 1)

# Ajouter des contraintes pour encourager un ordre séquentiel de matchs au sein de chaque pot
function encourage_sequential_matches(model, pot_start, pot_end)
    # Pour chaque équipe dans le pot
    for i in pot_start:pot_end
        next_team = i+1 <= pot_end ? i+1 : pot_start
        prev_team = i-1 >= pot_start ? i-1 : pot_end
        # Encourage l'équipe i à jouer contre l'équipe suivante et précédente dans le pot
        @constraint(model, sum(x[i, next_team, t] for t in 1:T) == 1) # Jouer contre l'équipe suivante une fois
        @constraint(model, sum(x[prev_team, i, t] for t in 1:T) == 1) # Jouer contre l'équipe précédente une fois
    end
end

# Encourager un ordre séquentiel de matchs pour chaque pot
encourage_sequential_matches(model, 1, 9)   # Pot A
encourage_sequential_matches(model, 10, 18) # Pot B
encourage_sequential_matches(model, 19, 27) # Pot C
encourage_sequential_matches(model, 28, 36) # Pot D


function encourage_inter_pot_matches(model, pot1_start, pot1_end, pot2_start, pot2_end)
    N_pot2 = pot2_end - pot2_start + 1 # Nombre d'équipes dans le pot2
    # Pour chaque équipe dans le pot1
    for i in pot1_start:pot1_end
        # Calcul de l'équipe cible dans le pot2 avec ajustement cyclique
        target_team_in_pot2 = pot2_start + ((i - pot1_start + 1) % N_pot2)
        
        # Contrainte pour que l'équipe i du pot1 joue contre l'équipe cible dans le pot2
        @constraint(model, sum(x[i, target_team_in_pot2, t] for t in 1:T) == 1)
    end
end

# Pot A vers Pot B et inversement
encourage_inter_pot_matches(model, 1, 9, 10, 18)
encourage_inter_pot_matches(model, 10, 18, 1, 9)

# Pot A vers Pot C et inversement
encourage_inter_pot_matches(model, 1, 9, 19, 27)
encourage_inter_pot_matches(model, 19, 27, 1, 9)

# Pot A vers Pot D et inversement
encourage_inter_pot_matches(model, 1, 9, 28, 36)
encourage_inter_pot_matches(model, 28, 36, 1, 9)

# Pot B vers Pot C et inversement
encourage_inter_pot_matches(model, 10, 18, 19, 27)
encourage_inter_pot_matches(model, 19, 27, 10, 18)

# Pot B vers Pot D et inversement
encourage_inter_pot_matches(model, 10, 18, 28, 36)
encourage_inter_pot_matches(model, 28, 36, 10, 18)

# Pot C vers Pot D et inversement
encourage_inter_pot_matches(model, 19, 27, 28, 36)
encourage_inter_pot_matches(model, 28, 36, 19, 27)


# Contrainte pour l'alternance stricte au début et à la fin
@constraint(model, strict_alternate_start[i in 1:N], sum(x[i, j, 1] + x[i, j, 2] for j in 1:N) == 1)
@constraint(model, strict_alternate_end[i in 1:N], sum(x[i, j, 7] + x[i, j, 8] for j in 1:N) == 1)

# Contrainte pour limiter les breaks à 1 maximum
for i in 1:N
    for t in 2:6
        @constraint(model, sum(x[i, j, t] + x[i, j, t+1] for j in 1:N) <= 1 + break_var[i, t])
        @constraint(model, sum(x[j, i, t] + x[j, i, t+1] for j in 1:N) <= 1 + break_var[i, t])
    end
    @constraint(model, sum(break_var[i, t] for t in 2:6) <= 1)
end

#=
# Équipes sans break
for i in [k for k in 3:N if !(k in [10, 11, 19, 20, 28, 29])]
    for t in 2:6
        @constraint(model, sum(x[i, j, t] + x[i, j, t+1] for j in 1:N) == 1)
        @constraint(model, sum(x[j, i, t] + x[j, i, t+1] for j in 1:N) == 1)
    end
end
    
# Contraintes pour limiter les breaks à 1 maximum pour A1, B1, C1 et D1

for t in 2:6
    @constraint(model, sum(x[1, j, t] + x[1, j, t+1] for j in 1:N) <= 1 + break_var[1, t])
    @constraint(model, sum(x[j, 1, t] + x[j, 1, t+1] for j in 1:N) <= 1 + break_var[1, t])
    @constraint(model, sum(x[10, j, t] + x[10, j, t+1] for j in 1:N) <= 1 + break_var[2, t])
    @constraint(model, sum(x[j, 10, t] + x[j, 10, t+1] for j in 1:N) <= 1 + break_var[2, t])
    @constraint(model, sum(x[19, j, t] + x[19, j, t+1] for j in 1:N) <= 1 + break_var[3, t])
    @constraint(model, sum(x[j, 19, t] + x[j, 19, t+1] for j in 1:N) <= 1 + break_var[3, t])
    @constraint(model, sum(x[28, j, t] + x[28, j, t+1] for j in 1:N) <= 1 + break_var[4, t])
    @constraint(model, sum(x[j, 28, t] + x[j, 28, t+1] for j in 1:N) <= 1 + break_var[4, t])
    @constraint(model, sum(x[2, j, t] + x[2, j, t+1] for j in 1:N) <= 1 + break_var[5, t])
    @constraint(model, sum(x[j, 2, t] + x[j, 2, t+1] for j in 1:N) <= 1 + break_var[5, t])
    @constraint(model, sum(x[11, j, t] + x[11, j, t+1] for j in 1:N) <= 1 + break_var[6, t])
    @constraint(model, sum(x[j, 11, t] + x[j, 11, t+1] for j in 1:N) <= 1 + break_var[6, t])
    @constraint(model, sum(x[20, j, t] + x[20, j, t+1] for j in 1:N) <= 1 + break_var[7, t])
    @constraint(model, sum(x[j, 20, t] + x[j, 20, t+1] for j in 1:N) <= 1 + break_var[7, t])
    @constraint(model, sum(x[29, j, t] + x[29, j, t+1] for j in 1:N) <= 1 + break_var[8, t])
    @constraint(model, sum(x[j, 29, t] + x[j, 29, t+1] for j in 1:N) <= 1 + break_var[8, t])
end

for i in 1:8
@constraint(model, sum(break_var[i, t] for t in 2:6) <= 1)
end
=#
#=
# Contraintes pour s'assurer qu'il y a exactement 1 jour avec 2 matchs pour chaque pot
@constraint(model, sum(two_matches_potA[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potB[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potC[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potD[t] for t in 1:T) == 1)

# Contraintes pour s'assurer que chaque jour a soit 1 soit 2 matchs pour chaque pot
for t in 1:T
    @constraint(model, sum(x[i, j, t] for i in 1:9, j in 1:9) == 1 + two_matches_potA[t])
    @constraint(model, sum(x[i, j, t] for i in 10:18, j in 10:18) == 1 + two_matches_potB[t])
    @constraint(model, sum(x[i, j, t] for i in 19:27, j in 19:27) == 1 + two_matches_potC[t])
    @constraint(model, sum(x[i, j, t] for i in 28:36, j in 28:36) == 1 + two_matches_potD[t])
end

# Contraintes pour chaque paire de pots
@constraint(model, sum(three_matches_AB[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_AC[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_AD[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_BC[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_BD[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_CD[t] for t in 1:T) == 2)


# Fonction pour ajouter une contrainte de matchs maximum entre deux pots par journée
function add_max_inter_pot_constraint(pot1_start, pot1_end, pot2_start, pot2_end, min_matches, max_matches)
    for t in 1:T
        @constraint(model, min_matches <= sum(x[i, j, t] for i in pot1_start:pot1_end, j in pot2_start:pot2_end) + 
                            sum(x[i, j, t] for i in pot2_start:pot2_end, j in pot1_start:pot1_end) <= max_matches)
    end
end

# Appliquer la contrainte pour chaque paire de pots avec un maximum de 3 matchs par journée
add_max_inter_pot_constraint(1, 9, 10, 18, 2, 3) # Pots A et B
add_max_inter_pot_constraint(1, 9, 19, 27, 2, 3) # Pots A et C
add_max_inter_pot_constraint(1, 9, 28, 36, 1, 3) # Pots A et D
add_max_inter_pot_constraint(10, 18, 19, 27, 1, 3) # Pots B et C
add_max_inter_pot_constraint(10, 18, 28, 36, 1, 3) # Pots B et D
add_max_inter_pot_constraint(19, 27, 28, 36, 1, 3) # Pots C et D



# Ajouter des contraintes pour encourager un ordre séquentiel de matchs au sein de chaque pot
function encourage_sequential_matches(model, pot_start, pot_end)
    # Pour chaque équipe dans le pot
    for i in pot_start:pot_end
        next_team = i+1 <= pot_end ? i+1 : pot_start
        prev_team = i-1 >= pot_start ? i-1 : pot_end
        # Encourage l'équipe i à jouer contre l'équipe suivante et précédente dans le pot
        for t in 1:T
            @constraint(model, sum(x[i, next_team, t] for t in 1:T) == 1) # Jouer contre l'équipe suivante une fois
            @constraint(model, sum(x[prev_team, i, t] for t in 1:T) == 1) # Jouer contre l'équipe précédente une fois
        end
    end
end

# Encourager un ordre séquentiel de matchs pour chaque pot
encourage_sequential_matches(model, 1, 9)   # Pot A
encourage_sequential_matches(model, 10, 18) # Pot B
encourage_sequential_matches(model, 19, 27) # Pot C
encourage_sequential_matches(model, 28, 36) # Pot D


@constraint(model, sum(break_var[i, t] for i in 1:N, t in 2:6) <= 11)


#@objective(model, Min, sum(break_var[i, t] for i in 1:N, t in 2:6))

=#

# Lancement de l'optimisation pour trouver une solution réalisable
optimize!(model)


# Vérifier si une solution a été trouvée
if termination_status(model) == MOI.OPTIMAL || termination_status(model) == MOI.FEASIBLE
    println("Une solution a été trouvée.")  

    # Créer une structure pour stocker le calendrier des matchs
    match_schedule = Dict()

    # Parcourir toutes les combinaisons d'équipes et de journées
    for t in 1:T
        for i in 1:N
            for j in 1:N
                if value(x[i, j, t]) > 0.5 # Si l'équipe i joue contre l'équipe j à la journée t
                    if !haskey(match_schedule, t)
                        match_schedule[t] = []
                    end
                    push!(match_schedule[t], (i, j))
                end
            end
        end
    end

    # Afficher le calendrier des matchs
    for t in 1:T
        println("Journée $t:")
        for match in match_schedule[t]
            println("Équipe $(match[1]) vs Équipe $(match[2])")
        end
    end
end

using CSV, DataFrames

# Fonction pour convertir le numéro d'équipe en nom
function team_name(team_number)
    if team_number <= 9
        return "A" * string(team_number)
    elseif team_number <= 18
        return "B" * string(team_number - 9)
    elseif team_number <= 27
        return "C" * string(team_number - 18)
    else
        return "D" * string(team_number - 27)
    end
end

# Créer un DataFrame pour stocker les matchs
df_matches = DataFrame(Day = Int[], Team1 = String[], Team2 = String[])

for t in 1:T
    for match in match_schedule[t]
        push!(df_matches, (t, team_name(match[1]), team_name(match[2])))
    end
end

# Sauvegarder le DataFrame dans un fichier CSV
CSV.write("match_schedule_symétrie.csv", df_matches)