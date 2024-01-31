using JuMP, Cbc

# Création du modèle avec le solveur Cbc
model = Model(Cbc.Optimizer)

# Nombre d'équipes et de journées
N = 36
T = 8

# Définition des variables
@variable(model, x[1:N, 1:N, 1:T], Bin)

# Variables supplémentaires pour contrôler les breaks
@variable(model, break_var[1:N, 2:6], Bin)


# Variables supplémentaires pour les matchs de chaque pot
@variable(model, two_matches_potA[1:T], Bin)
@variable(model, two_matches_potB[1:T], Bin)
@variable(model, two_matches_potC[1:T], Bin)
@variable(model, two_matches_potD[1:T], Bin)

# Variables pour compter les matchs entre les pots pour chaque journée
@variable(model, matches_AB[1:T] >= 0)
@variable(model, matches_AC[1:T] >= 0)
@variable(model, matches_AD[1:T] >= 0)
@variable(model, matches_BC[1:T] >= 0)
@variable(model, matches_BD[1:T] >= 0)
@variable(model, matches_CD[1:T] >= 0)

# Variables pour représenter la déviation du nombre de matchs par rapport à une cible
@variable(model, deviation_AB[1:T] >= 0)
@variable(model, deviation_AC[1:T] >= 0)
@variable(model, deviation_AD[1:T] >= 0)
@variable(model, deviation_BC[1:T] >= 0)
@variable(model, deviation_BD[1:T] >= 0)
@variable(model, deviation_CD[1:T] >= 0)

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

# Contrainte pour l'alternance stricte au début et à la fin
@constraint(model, strict_alternate_start[i in 1:N], sum(x[i, j, 1] + x[i, j, 2] for j in 1:N) == 1)
@constraint(model, strict_alternate_end[i in 1:N], sum(x[i, j, 7] + x[i, j, 8] for j in 1:N) == 1)

# Contrainte pour limiter les breaks à 1 maximum
for i in 1:N
    for t in 2:6
        @constraint(model, sum(x[i, j, t] + x[i, j, t+1] for j in 1:N) <= 1 + break_var[i, t])
    end
    @constraint(model, sum(break_var[i, t] for t in 2:6) <= 1)
end

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


average_matches = 18 / T # Nombre moyen de matchs entre deux pots sur les journées

# Contraintes pour définir les variables type matches_AB
function define_matches_pq(pot1_start, pot1_end, pot2_start, pot2_end, matches_pq, deviation_pq)
    for t in 1:T
        @constraint(model, matches_pq[t] == sum(x[i, j, t] for i in pot1_start:pot1_end, j in pot2_start:pot2_end) + 
                            sum(x[i, j, t] for i in pot2_start:pot2_end, j in pot1_start:pot1_end))
        @constraint(model, deviation_pq[t] >= average_matches - matches_pq[t])
    end
end

# Appliquer la contrainte pour chaque paire de pots avec un maximum de 3 matchs par journée
define_matches_pq(1, 9, 10, 18, matches_AB, deviation_AB) # Pots A et B
define_matches_pq(1, 9, 19, 27, matches_AC, deviation_AC) # Pots A et C
define_matches_pq(1, 9, 28, 36, matches_AD, deviation_AD) # Pots A et D
define_matches_pq(10, 18, 19, 27, matches_BC, deviation_BC) # Pots B et C
define_matches_pq(10, 18, 28, 36, matches_BD, deviation_BD) # Pots B et D
define_matches_pq(19, 27, 28, 36, matches_CD, deviation_CD) # Pots C et D


# Fonction objective pour minimiser la variation des matchs entre les pots

@objective(model, Min, 
    sum(deviation_AB[t] for t in 1:T) +
    sum(deviation_AC[t] for t in 1:T) +
    sum(deviation_AD[t] for t in 1:T) +
    sum(deviation_BC[t] for t in 1:T) +
    sum(deviation_BD[t] for t in 1:T) +
    sum(deviation_CD[t] for t in 1:T)
)



# Lancement de l'optimisation pour trouver une solution réalisable
optimize!(model)