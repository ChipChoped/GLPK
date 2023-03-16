import mip

class Graph:
    def __init__(self, nbNode, edges):
        self.edges = list(edges)
        self.nbNode = nbNode
        self.voisins = [[] for i in range(nbNode)]
        for u, v in self.edges:
            self.voisins[u-1].append(v-1)
            self.voisins[v-1].append(u-1)    
        

    def algoGlouton(self):
        degrees = [len(self.voisins[i]) for i in range(self.nbNode)]
        order = sorted(range(self.nbNode), key=lambda i: degrees[i])
        sommetAjouter = []
        for i in order:
            if all(j not in self.voisins[i] for j in sommetAjouter):
                sommetAjouter.append(i)
        return sorted(sommetAjouter)

    def OptimisationLocal(self, N):
        degrees = [len(self.voisins[i]) for i in range(self.nbNode)]
        order = sorted(range(self.nbNode), key=lambda i: degrees[i])
        selected=[]
        while True:
            # Recherche des N premiers sommets non sélectionnés et non voisins de sommets sélectionnés
            candidats=[]
            for i in order:
                if i not in selected :
                    #if all(j not in selected for j in self.voisins[i]): 
                        candidats.append(i)
            candidats=candidats[:N]
            print(candidats)
                        
            # S'il n'y a plus de candidats, on a atteint le maximum de sommets sélectionnés
            if candidats == []:
                break

            # Formulation du PLNE pour sélectionner les sommets à ajouter parmi les candidats
            m = mip.Model("PLNE")
            x = [m.add_var(var_type=mip.BINARY) for i in candidats]
            m.objective = mip.maximize(mip.xsum(x[i] for i in range(len(candidats))))
            '''
            for i in candidats:
                voisinI=[]
                for j in self.voisins[i]:
                    if j in candidats and j < len(x):
                        voisinI.append(x[j])
                m += mip.xsum(voisinI) <= 1

            '''
            for i in candidats:
                voisinI=[]
                for j in self.voisins[i]:
                    if j in candidats:
                        voisinI.append(x[candidats.index(j)])
                m += mip.xsum(voisinI) <=1

            m.optimize()

            # Ajout des sommets sélectionnés dans la liste de sélection
            for i in range(len(candidats)):
                if x[i].x > 0.9:
                    selected.append(candidats[i])
                    if len(selected) == N:
                        break

        return sorted(selected)        



def readFile(file):
    edges = []
    nbNode=0
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('p'):
                nbNode =  int((line[2:].split())[1])
            if line.startswith('e'):
                nodes =  line[2:].split()
                if(nodes[0]<nodes[1]):
                    edges.append((int(nodes[0]), int(nodes[1])))
                else:
                    edges.append((int(nodes[1]), int(nodes[0])))
    return nbNode,edges


def complementGraph(file):
    nbNode,edges = readFile(file)    
    all_edges = set()
    for i in range(1, nbNode+1):
        for j in range(i, nbNode+1):
            if(i!=j):
                all_edges.add((i, j))
    complement_edges =  all_edges - set(edges)
    G=Graph(nbNode,complement_edges)
    return G


if __name__ == "__main__":
    graphe=complementGraph("graphe/DIMACS_subset_ascii/C125.9.clq")
    N=20
    sol1=graphe.algoGlouton()
    print("Solution Glouton: ",len(sol1))

    sol2=graphe.OptimisationLocal(N)
    print("Optimisation local: ",len(sol2))

    
    ok=set()
    for i in sol2:
        for j in sol2:
            if j>i and j in graphe.voisins[i]:
                ok.add(i)
    print(len(ok))