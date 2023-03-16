param nbVertex, integer;

set VERTICES :=1..nbVertex;

param graph{i1 in VERTICES, i2 in VERTICES};

#variables de decision
var x{i in VERTICES}, binary;

maximize obj :
  sum{i in VERTICES} x[i];

#contraintes
s.t. C_clique{ i1 in VERTICES, i2 in VERTICES : i1 < i2 && graph[i1,i2] == 1}:
x[i1] + x[i2] <= 1;
s.t. C_clique2{ i1 in VERTICES, i2 in VERTICES, i3 in VERTICES : graph[i1,i2] == 1 && graph[i2, i3] == 1 && graph[i1, i3] == 1}:
x[i1] + x[i2] + x[i3] <= 1;

solve;

printf "\n--------------------------------\n";
printf "Nombre de sommets dans le graphe stable : %g\n", obj;
printf "Liste des sommets selectionnes :\n";
for {i in VERTICES : x[i]>0}
    printf " %3s ", x[i];
printf "\n";
printf "--------------------------------\n";
end;

