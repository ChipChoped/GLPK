
param M:=24*60;
param nbTIC, integer;
param nbINT, integer;

param nbTACHES:=nbTIC+nbINT;

set TIC :=1..nbTIC;
set INT :=1..nbINT;
set TACHES := 1..nbTACHES;
set TACHESTIC := (nbINT+1)..nbTACHES;


param t_start{i in TIC};
param t_end{i in TIC};

param duree{i in INT};
param date{i in INT};
param s_min{i in INT};
param s_max{i in INT};
param penalite{i in INT};

param C{i in TIC, j in TACHES};
param T{i in TACHES, j in TACHES};
param D{i in TACHES, j in TACHES};

#variables de decision

var u{i1 in TACHES, i2 in TACHES, j in TIC}, binary;

var v{i in TACHES}, binary;

var t{i in INT};

#contraintes


# de tournees
s.t. C_tournee1{i in INT} :
 sum{j in TIC, l in TACHES} u[l,i,j] = v[i];

s.t. C_tournee2{i in INT, j in TIC} :
 sum{l in TACHES} u[l,i,j]=  sum{l in TACHES} u[i,l,j];

s.t. C_debut1{j in TIC, i1 in TACHES}:
u[i1,i1,j]=0;

s.t. C_debut2{j in TIC, i1 in TIC, i2 in TACHES : i1<>j}:
u[i1+nbINT,i2,j]=0;

s.t. C_debut3{j in TIC, i1 in TIC, i2 in TACHES : i1<>j}:
u[i2,i1+nbINT,j]=0;

s.t. C_depart4{j in TIC, i in INT}:
(sum{l in INT} u[i,l,j] ) <= (sum{l in INT} u[nbINT+j,l,j]);


# de Competence

s.t. C_competence{j in TIC, i in TACHES}:
 sum{l in TACHES} u[l,i,j]<=C[j,i];


# de debut et de fin de journee

s.t. C_debut_fin_jour1{j in TIC}:
 sum{l in INT} u[nbINT+j,l,j]<=1;

s.t. C_debut_fin_jour2{j in TIC}:
 sum{l in INT} (u[l,nbINT+j,j]-u[nbINT+j,l,j])=0;

s.t. C_debut_fin_jour3{j in TIC, i in INT}:
t_start[j]+T[nbINT+j,i] <= t[i]+(1-u[nbINT+j,i,j])*M;

s.t. C_debut_fin_jour4{j in TIC, i in INT}:
t[i]+duree[i]+T[i,nbINT+j]<=t_end[j]+(1-u[i,nbINT+j,j])*M;

# de respect de fenetre de temps

s.t. C_fen_tps1{j in TIC, i1 in INT, i2 in INT}:
t[i1]+duree[i1]+T[i1,i2]<=t[i2]+(1-u[i1,i2,j])*M;

s.t. C_fen_tps2{i1 in INT}:
 t[i1]>=s_min[i1];

s.t. C_fen_tps3{i1 in INT}:
 t[i1]<=s_max[i1];


##############################################

# Objectif

var sum1;
var sum2;
var sum3;
var objectif;

s.t. C_sum1:
sum1=sum{j in TIC, i in INT} D[nbINT+j,i]*u[nbINT+j,i,j];

s.t. C_sum2:
sum2=sum{j in TIC, i1 in INT, i2 in INT} D[i1,i2] *u[i1,i2,j];

s.t. C_sum3:
sum3=sum{j in TIC, i in INT} D[i,nbINT+j]*u[i,nbINT+j,j];

s.t. C_obj:
objectif=sum1+sum2+sum3+ sum{i in INT} penalite[i]*(1-v[i]);

minimize obj: objectif;

solve;

printf "    L=%g\n", objectif;
printf "    S1=%g\n", sum1;
printf "    S2=%g\n", sum2;
printf "    S3=%g\n", sum3;

printf "--------------------------------\n";
printf "Liste des variables de decision non nulles :\n";
for {j in TIC, i1 in TACHES, i2 in TACHES : u[i1,i2,j]<>0}
    printf "    u[%3s %3s %3s]=%4s => %5s \n", i1, i2, j, u[i1,i2,j], D[i1,i2];
printf "--------------------------------\n";
printf "    L= %g\n", objectif;

end;

