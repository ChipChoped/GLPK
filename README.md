## Questions

#### Lancer un fichier mod sur un dossier de données
> python3 src/script.py src/fichier.mod Data (--options)

### 1.
> Le graphe à 100 nœuds de densité 3 est le seul graphe à répondre au-dessus de 10 secondes (23.4)

> Le calcul devient plus difficile à partir de n = 80

### 2.
> Le graphe complémentaire à 100 nœuds de densité 3 est le seul graphe à répondre au-dessus de 10 secondes (25)

> On retrouve les mêmes résultats qu'avec le calcul de la max clique mais avec bien l'inversion sur les graphes et leur complémentaire 

### 3.
> On retrouve la règle où le nombre de sommets retenu est >= n/2

### 4.
> maxStable : Temps pratiquement à 0 seconde et seulement deux solutions non entières
> maxstablesV2 : Plus un graphe a de nœuds plus ils prennent de temps à être résolu et seulement quatre solutions entières

### 6.
> c.f. src/max_stable.py

### 7.
> python3 src/max_stable graph_path N

> Dans de très grands graphes, le glouton donne des solutions plus grandes. Sûrement une erreur dans l'algorithme.

#### Optimisation locale
> Trier les nœuds par leur degré
> Prendre les N premiers noeuds en candidats
> Executer la PLNE
> Supprimer les noeuds voisins des noeuds choisis pendant la PLNE
> Recommancer sur les N suivant noeuds restants

