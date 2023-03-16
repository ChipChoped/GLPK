param nbItems ; #number of items 

set Items :=1..nbItems;

param costItem{i in Items}; #cost of items 

param weightItem{i in Items}; #weight of items

param capacity; #knapsack capacity

#variables 
var x{Items} binary; 

#objectif 
maximize obj :sum {i in Items} costItem[i]*x[i] ; 

#contraintes 
subject to 
capacityConstraint : sum{i in Items} weightItem[i]*x[i] <= capacity ;

solve;

printf "The knapsack contains the items:\n";
printf {i in Items : x[i] == 1} " %i", i;
printf "\n";


data; 

param nbItems := 5; 

param costItem := 
1 12
2 15
3 5
4 16
5 17; 

param weightItem :=
1 2
2 6
3 1
4 7
5 8; 

param capacity := 20; 

end;
