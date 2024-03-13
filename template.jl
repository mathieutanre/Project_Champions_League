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

# Variables supplémentaires pour contrôler les repétitions BB --> Tourne dans le vide
#@variable(model, repetBB_var[1:N, 1:7], Bin)
#@variable(model, repetCC_var[1:N, 1:7], Bin)
#@variable(model, repetDD_var[1:N, 1:7], Bin)

# Variables supplémentaires pour contrôler les suites de 3 matchs AB et CD
#@variable(model, repetCD3_var[1:N, 1:6], Bin)
#@variable(model, repetAB3_var[1:N, 1:6], Bin)


# Variables supplémentaires pour les matchs de chaque pot
@variable(model, two_matches_potA[1:T], Bin)
@variable(model, two_matches_potB[1:T], Bin)
@variable(model, two_matches_potC[1:T], Bin)
@variable(model, two_matches_potD[1:T], Bin)

# Variables supplémentaires pour les matchs entre les pots A et B et d'autre part C et D
@variable(model, three_matches_potsAB[1:T], Bin)
@variable(model, three_matches_potsCD[1:T], Bin)


# Contrainte : une équipe ne peut pas jouer contre elle-même
@constraint(model, no_self_play[i in 1:N, t in 1:T], x[i, i, t] == 0)

# Contrainte : une équipe joue au plus 1 fois contre chaque autre équipe
@constraint(model, max_one_game[i in 1:N, j in 1:N; i != j], sum(x[i, j, t] + x[j, i, t] for t in 1:T) <= 1)

# Contrainte : chaque équipe joue exactement un match par journée
@constraint(model, one_game_per_day[t in 1:T, i in 1:N], sum(x[i, j, t] + x[j, i, t] for j in 1:N) == 1)

# Contraintes spécifiques pour chaque pot
for i in 1:N
    for pot_start in 1:9:28
        @constraint(model, sum(x[i, j, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
        @constraint(model, sum(x[j, i, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
    end
end

# Contrainte pour s'assurer de l'homogénéité de la difficulté au cours du temps
 #On s'assure d'avoir exactement 2 matchs contre A et B les quatres premiers jours
for i in 1:N
    @constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 1:18 for t in 1:4) == 2)
end






#On peut attribuer une difficulté aux matchs contre A = 12 contre B = 10 contre C = 8 contre D=6
#Difficulté totale = 2*(15+10+8+5) = 76 car on joue deux fois contre toutes les catégories
# 3*76 / 8 = 28,5
# on peut essayer de demander une difficulté comprise entre 21 et 35 pour toute période de trois matchs comme res entier entre 7 et 8
# A verifier: est ce que cela évite les effets de carry over -> on ne peut pas avoir deux fois A dans un laps de temps de 3 jours ok
# Solution en 347s

#for i in 1:N
#    for t in 1:(T-2)
#        @constraint(model, 21 <= 
#            15 * sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2] for j in 1:9) + 
#            10 * sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2] for j in 10:18) + 
#            8 * sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2] for j in 19:27) + 
#            5 * sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2] for j in 28:N) <= 35)
#    end
#end




#jouer exactement une fois contre 1 equipe du pot A dans la première moitié = IMPOSSIBLE
#for i in 1:N
#    @constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 1:9 for t in 1:4) == 1)
#    @constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 28:36 for t in 1:4) == 1)
#end



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


#Contrainte sur le nombre de break, on cherche une solution a 4 break, une chaque pour groupe
@constraint(model, sum(break_var[i, t] for i in 1:9, t in 2:6) <= 1)
@constraint(model, sum(break_var[i, t] for i in 10:18, t in 2:6) <= 1)
@constraint(model, sum(break_var[i, t] for i in 19:27, t in 2:6) <= 1)
@constraint(model, sum(break_var[i, t] for i in 28:36, t in 2:6) <= 1)


# Contraintes pour s'assurer qu'il y ait exactement 1 jour avec 2 matchs intra pot pour chaque pot
@constraint(model, sum(two_matches_potA[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potB[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potC[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potD[t] for t in 1:T) == 1)

# Contraintes pour s'assurer que chaque jour on ait ou bien 1 ou bien 2 matchs pour chaque pot
for t in 1:T
    @constraint(model, sum(x[i, j, t] for i in 1:9, j in 1:9) == 1 + two_matches_potA[t])
    @constraint(model, sum(x[i, j, t] for i in 10:18, j in 10:18) == 1 + two_matches_potB[t])
    @constraint(model, sum(x[i, j, t] for i in 19:27, j in 19:27) == 1 + two_matches_potC[t])
    @constraint(model, sum(x[i, j, t] for i in 28:36, j in 28:36) == 1 + two_matches_potD[t])
end


# Contraintes pour s'assurer qu'il y a exactement 2 jours avec 3 matchs inter-pots pour les couples (A,B) et (C,D)
@constraint(model, sum(three_matches_potsAB[t] for t in 1:T) == 2)
#@constraint(model, sum(three_matches_potsCD[t] for t in 1:T) == 2)


# Contraintes pour s'assurer que chaque jour a ou bien 2 ou bien 3 matchs inter-pots (A,B) et (c,D)
for t in 1:T
    @constraint(model, sum(x[i, j, t] + x[j, i, t] for i in 1:9, j in 10:18) == 2 + three_matches_potsAB[t])
 #   @constraint(model, sum(x[i, j, t] + x[j, i ,t] for i in 19:27, j in 28:36) == 2 + three_matches_potsCD[t])
end

# Fonction pour ajouter une contrainte de matchs minimum maximum entre deux pots par journée
function add_max_inter_pot_constraint(pot1_start, pot1_end, pot2_start, pot2_end, min_matches, max_matches)
    for t in 1:T
        @constraint(model, min_matches <= sum(x[i, j, t] + x[j, i, t] for i in pot1_start:pot1_end, j in pot2_start:pot2_end)
                 <= max_matches)
    end
end


# Appliquer la contrainte pour chaque paire de pots avec un maximum de 3 matchs par journée, (non obligatoire
#                                                                                              pour les pots A et B et C et D)
#add_max_inter_pot_constraint(1, 9, 10, 18, 2, 3) # Pots A et B 
add_max_inter_pot_constraint(1, 9, 19, 27, 2, 3) # Pots A et C
add_max_inter_pot_constraint(1, 9, 28, 36, 1, 3) # Pots A et D
add_max_inter_pot_constraint(10, 18, 19, 27, 1, 3) # Pots B et C
add_max_inter_pot_constraint(10, 18, 28, 36, 1, 3) # Pots B et D
#add_max_inter_pot_constraint(19, 27, 28, 36, 1, 3) # Pots C et D



# Ajouter des contraintes pour imposer un ordre séquentiel de matchs au sein de chaque pot
# Par exemple A1 joue contre A2 qui joue contre A3 etc
function encourage_sequential_matches(model, pot_start, pot_end)
    # Pour chaque équipe dans le pot
    for i in pot_start:pot_end
        next_team = i+1 <= pot_end ? i+1 : pot_start
        prev_team = i-1 >= pot_start ? i-1 : pot_end
        # On impose à l'équipe i de jouer contre l'équipe suivante et précédente dans le pot
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






# Fonction pour ajouter la contrainte d'éviter les matchs consécutifs entre différents pots 
#distance de 3 matchs entre deux matchs contre un le pot A et D
function add_no_consecutive_inter_pot_matches_constraint_3(pot_start, pot_end)
    for i in 1:N
        for t in 1:(T-2)
            @constraint(model, sum(x[i, j, t] + x[i, j, t+1] + x[i, j, t+2] + x[j, i, t] + x[j, i, t+1] + x[j, i, t+2] for j in pot_start:pot_end) <= 1)
        end
    end
end
#distance de 2 maatchs entre deux matchs contre les pots B et D
function add_no_consecutive_inter_pot_matches_constraint_2(pot_start, pot_end)
    for i in 1:N
        for t in 1:(T-1)
            @constraint(model, sum(x[i, j, t] + x[i, j, t+1] + x[j, i, t] + x[j, i, t+1] for j in pot_start:pot_end) <= 1)
        end
    end
end

# Appliquer la contrainte pour tous les pots pas de répétitino AA ou DD
add_no_consecutive_inter_pot_matches_constraint_2(1, 9)   # avec Pot A
add_no_consecutive_inter_pot_matches_constraint_2(28, 36) # avec Pot D
#add_no_consecutive_inter_pot_matches_constraint_2(10, 18) # avec Pot B
#add_no_consecutive_inter_pot_matches_constraint_3(19, 27) # avec pot C







# Contrainte pour limiter les breaks à 1 maximum par équipe BB CC ou DD


#for i in 1:N
#    for t in 1:7
#        @constraint(model, sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] for j in 10:18) <= 1 + repetBB_var[i, t])
#        @constraint(model, sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] for j in 19:27) <= 1 + repetCC_var[i, t])
#        @constraint(model, sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] for j in 28:36) <= 1 + repetDD_var[i, t])
#    end
#    for t in 1:5
#        @constraint(model, repetBB_var[i,t] + repetBB_var[i,t+1] + repetBB_var[i,t+2] +
#                           repetCC_var[i,t] + repetCC_var[i,t+1] + repetCC_var[i,t+2] +
#                           repetDD_var[i,t] + repetDD_var[i,t+1] + repetDD_var[i,t+2] <= 2)
#    end
#end


#    @constraint(model, sum(repetBB_var[i, t] for t in 1:7) <= 1)
#    @constraint(model, sum(repetCC_var[i, t] for t in 1:7) <= 1)
#    @constraint(model, sum(repetDD_var[i, t] for t in 1:7) <= 1)
#end



#for i in 1:N
#    @constraint(model, sum(repetBB_var[i, t] + repetCC_var[i, t]  for t in 1:7) <= 1)  #Une seule répétition possible
#end                                                                                                         #Pas de CC ---- DD par exemple
# 


#for i in 1:N
     #Assurer que l'équipe i joue contre une équipe du pot spécifié pendant les 4 premières journées = 
     #on empeche AA ou DD au début et à la fin
    #@constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 28:36, t in 7:8) <= 1)
    #@constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 28:36, t in 1:2) <= 1)
    #@constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 19:27, t in 7:8) <= 1)
    #@constraint(model, sum(x[i, j, t] + x[j, i, t] for j in 19:27, t in 1:2) <= 1)
#end


#Empecher de jouer 3 fois d'affilé contre (C ou D) ou (A ou B)

#for i in 1:N
#    for t in 1:6
#    @constraint(model, sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2]
#      for j in 19:36) <= 2)
#    @constraint(model, sum(x[i, j, t] + x[j, i, t] + x[i, j, t+1] + x[j, i, t+1] + x[i, j, t+2] + x[j, i, t+2]
#      for j in 1:18) <= 2)
#    end
#end




#@objective(model, Min, sum(break_var[i, t] for i in 1:N, t in 2:6))




#--------------------------------------------SOLVEUR------------------------------------------------------------------------------------





# Lancement de l'optimisation pour trouver une solution réalisable
optimize!(model)

# Vérifier si une solution a été trouvée
if termination_status(model) == MOI.OPTIMAL || termination_status(model) == MOI.FEASIBLE
    println("Une solution a été trouvée.")

#    breaks = 0
#    breaks = sum(value(break_var[i, t]) for i in 1:N for t in 2:6 if value(break_var[i, t]) > 0.5)
#    println("Nombre de breaks : $(breaks)")    

#    repetitionBB = 0
#    repetitionBB = sum(value(repetBB_var[i, t]) for i in 1:N for t in 1:7 if value(repetBB_var[i, t]) > 0.5)
#    println("Nombre de répétition B-B : $(repetitionBB)") 
#    repetitionCC = 0
#    repetitionCC = sum(value(repetCC_var[i, t]) for i in 1:N for t in 1:7 if value(repetCC_var[i, t]) > 0.5)
#    println("Nombre de répétition C-C : $(repetitionCC)") 
#    repetitionDD = 0
#    repetitionDD = sum(value(repetCC_var[i, t]) for i in 1:N for t in 1:7 if value(repetDD_var[i, t]) > 0.5)
#    println("Nombre de répétition D-D : $(repetitionDD)") 


    #Créer une structure pour stocker le calendrier des matchs
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
CSV.write("match_schedule_test.csv", df_matches)

