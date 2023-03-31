param nbVertex;                   # nombre de sommets
param nbColorFeasible;            # nombre de couleurs possibles
param cardCliqueMax;              # taille maximale des cliques

# ensembles
set V := 1..nbVertex;             # ensemble de sommets
set E := {i in V, j in V};         # ensemble d arêtes
set C := 1..nbVertex;      # ensemble de couleurs

# paramètres
param graph{(i,j) in E}, binary;  # matrice d adjacence du graphe
param cliqueColors{i in V};  # matrice de couleurs des cliques

# variables de décision
var z{V,C}, binary;              # z[i,c]=1 si le sommet i est de couleur c
var y;                           # nombre total de couleurs utilisées

# objectif
minimize num_colors: y;

# contraintes
s.t. c1{v in V}: sum{c in C} z[v,c] >= 1;  # chaque sommet est colorié avec une seule couleur
s.t. c2{c in C, v in V}: c * z[v,c] <=y ;  
s.t. c3{c in C, i in V, j in V : i<j && graph[i,j]==1}: z[i,c]+z[j,c] <= 1;
s.t. c4: y >=0;
s.t. c5{i in V : cliqueColors[i]>0}: z[i,cliqueColors[i]] = 1;

# Symetrie
#s.t. c6: z[1,1] = 1;  

solve;

printf "\n--------------------------------\n";
printf "Nombre total de couleurs utilisées : %g\n", num_colors;
end;
