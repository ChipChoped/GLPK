### 1.
> Le graphe à 100 nœuds de densité 3 est le seul graphe à répondre au-dessus de 10 secondes (23.4)

> Le calcul devient plus difficile à partir de n = 80

### 2.
> Le graphe complémentaire à 100 nœuds de densité 3 est le seul graphe à répondre au-dessus de 10 secondes (25)

> On retrouve les mêmes résultats qu'avec le calcul de la max clique mais avec bien l'inversion sur les graphes et leur complémentaire 

### 3.
> On retrouve la règle où le nombre de sommets retenu est >= n/2

### 7. Optimisation Locale
> Trier les nœuds par leur degré
> Prendre les N premiers noeuds en candidats
> Executer la PLNE
> Supprimer les noeuds voisins des noeuds choisis pendant la PLNE
> Recommancer sur les N suivant noeuds restants