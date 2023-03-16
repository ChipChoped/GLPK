param nbItems ; #number of items 

set Items :=1..nbItems;

param costItem{i in Items}; #cost of items 

param weightItem{i in Items}; #weight of items

param capacity; #knapsack capacity

#variables 
var x{Items}, >=0, <=1; 

#objectif 
maximize obj :sum {i in Items} costItem[i]*x[i] ; 

#contraintes 
subject to 
capacityConstraint : sum{i in Items} weightItem[i]*x[i] <= capacity ;

solve;

printf "The continuous knapsack contains the items:\n";
printf {i in Items : x[i] > 0} " item %i in quantity %f \n", i, x[i];
printf "\n";

end;
