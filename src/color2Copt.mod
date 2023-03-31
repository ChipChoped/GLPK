 
param nbVertex;                   # nombre de sommets
param nbColorFeasible;            # nombre de couleurs possibles
param cardCliqueMax;              # taille maximale des cliques

# ensembles
set V := 1..nbVertex;             # ensemble de sommets
set E := {i in V, j in V};     # ensemble d arêtes
set C := 1..cardCliqueMax;      # ensemble de couleurs

# paramètres
param graph{(i,j) in E}, binary;  # matrice d adjacence du graphe
param cliqueColors{i in V};  # matrice de couleurs des cliques

# variables de décision
var z{V,C}, binary;              # z[i,c]=1 si le sommet i est de couleur c
var y{C}, binary;                # 1 si la couleur c est utilisées

minimize num_colors: sum {c in C} y[c];
s.t. c1{v in V}: sum{c in C} z[v,c] >= 1;  
s.t. c2{c in C,v in V}: z[v,c] <= y[c];  
s.t. c3{c in C, i in V, j in V : i<j && graph[i,j]==1}: z[i,c]+z[j,c] <= 1;
s.t. c4{i in V : cliqueColors[i]>0}: z[i,cliqueColors[i]] = 1;

# Symetrie
#s.t. c4: z[1,1] = 1;  

solve;

printf "\n--------------------------------\n";
printf "Nombre total de couleurs utilisées : %g\n", num_colors;
end;
