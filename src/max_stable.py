import sys
import mip
import time
import random
from mip import Model, MAXIMIZE, CBC, BINARY, OptimizationStatus


class Graph:
    def __init__(self, vertices_number, edges):
        self.edges = list(edges)
        self.vertices_number = vertices_number
        self.adjacent_vertices = [[] for i in range(vertices_number)]

        for u, v in self.edges:
            self.adjacent_vertices[u - 1].append(v - 1)
            self.adjacent_vertices[v - 1].append(u - 1)

    def greedy_algorithm(self) -> list[int]:

        degrees = [len(self.adjacent_vertices[i]) for i in range(self.vertices_number)]
        order = sorted(range(self.vertices_number), key=lambda i: degrees[i])
        added_vertices = []

        for i in order:
            if all(j not in self.adjacent_vertices[i] for j in added_vertices):
                added_vertices.append(i)

        return sorted(added_vertices)

    def local_optimization(self, n: int, majDegree=False, orderRandom=False, orderMix=False) -> tuple[list[int], OptimizationStatus, int, float, float]:
        degrees = [len(self.adjacent_vertices[i]) for i in range(self.vertices_number)]
        order = sorted(range(self.vertices_number), key=lambda i: degrees[i])
        selected = []
        status = -1
        iterations_count = 0

        clock_start = 0
        clock_end = 0
        cpu_start = 0
        cpu_end = 0

        if orderRandom:
            random.shuffle(order)

        if orderMix:
            degre = [0 for i in order]
            nMin=len(self.adjacent_vertices[0])
            nMax=len(self.adjacent_vertices[0])
            for voisin in self.adjacent_vertices:
                if nMin>len(voisin):
                    nMin=len(voisin)
                if nMax<len(voisin):
                    nMax=len(voisin)
            for i in range(len(order)):
                degre[i]=random.randint(0,int(0.5*(nMax-nMin)))
            order = sorted(range(self.vertices_number), key=lambda i: degrees[i])
            
        while True:
            candidates = []

            if len(order) < n:
                n = len(order)

            for i in range(n):
                if all(j not in selected for j in self.adjacent_vertices[order[i]]):
                    candidates.append(order[i])

            order = order[n:len(order)]

            # S'il n'y a plus de candidates, on a atteint le maximum de sommets sélectionnés
            if not candidates:
                break

            # Formulation du PLNE pour sélectionner les sommets à ajouter parmi les candidates
            model = Model("PLNE", MAXIMIZE, CBC)
            x = [model.add_var(var_type=BINARY) for i in candidates]
            model.objective = mip.maximize(mip.xsum(x[i] for i in range(len(candidates))))

            for i in candidates:
                for j in self.adjacent_vertices[i]:
                    if j in candidates:
                        model += x[candidates.index(i)] + x[candidates.index(j)] <= 1

            clock_start = time.time()
            cpu_start = time.process_time()
            status = model.optimize()
            clock_end = time.time()
            cpu_end = time.process_time()
            iterations_count += 1

            to_remove = set()

            # Ajout des sommets sélectionnés dans la liste de sélection
            for i in range(len(candidates)):
                if float(x[i].x) > 0.9:
                    selected.append(candidates[i])

                    for j in order:
                        if j in self.adjacent_vertices[candidates[i]]:
                            to_remove.add(j)

                    to_remove.add(candidates[i])

                    if len(selected) == n:
                        break

            order = [r for r in order if r not in to_remove]

            # Maj des degrées
            if majDegree:
                degrees=self.maj_degre(selected,order)
                order = sorted(range(len(order)), key=lambda i: degrees[i])
            

        return sorted(selected), status, iterations_count, clock_end - clock_start, cpu_end - cpu_start

    def maj_degre(self, selected, order):
        degre = [0 for i in order]
        for i in order:
            for voisin in self.adjacent_vertices[i]:
                if voisin not in selected and voisin in order:
                    degre[order.index(i)]+=1
        return degre

    def tabu_search(self, init_stable, iterations: int, tabu_max_length: int, k: int = 1):
        tabu_vertices = []
        neighborhood = []

        print(init_stable)

        degrees = [len(self.adjacent_vertices[i]) for i in range(self.vertices_number)]
        order = sorted(range(self.vertices_number), key=lambda i: degrees[i])

        order = [r for r in order if r not in init_stable]

        max_stable = init_stable.copy()

        for i in range(iterations):
            found_vertex = False

            for u in order:
                if all(u not in self.adjacent_vertices[v] for v in init_stable) and u not in tabu_vertices:
                    init_stable.append(u)
                    del order[order.index(u)]
                    found_vertex = True
                    break

            if not found_vertex:
                if len(tabu_vertices) == tabu_max_length:
                    tabu_vertices.pop(0)
                    order = sorted(range(self.vertices_number), key=lambda i: degrees[i])
                    order = [r for r in order if r not in init_stable]
                    order = [r for r in order if r not in tabu_vertices]

                rand = random.randint(0, len(init_stable) - 1)
                tabu_vertices.append(init_stable[rand])
                del init_stable[rand]

            if len(init_stable) > len(max_stable):
                max_stable = init_stable.copy()

        return max_stable

    def verif_stable(self, solution):
        vertices = range(self.vertices_number)
        vertices = [r for r in vertices if r not in solution]

        for v in solution:
            if all(v in self.adjacent_vertices[u] for u in vertices):
                return False

        return True


def read_file(file: str) -> tuple[int, list[tuple[int, int]]]:
    edges = []
    vertices_number = 0

    with open(file, 'r') as f:
        for line in f:
            if line.startswith('p'):
                vertices_number = int((line[2:].split())[1])
            if line.startswith('e'):
                vertex = line[2:].split()
                if vertex[0] < vertex[1]:
                    edges.append((int(vertex[0]), int(vertex[1])))
                else:
                    edges.append((int(vertex[1]), int(vertex[0])))

    return vertices_number, edges


def parse_graph(file: str) -> tuple[Graph, Graph]:
    vertices_number, edges = read_file(file)
    all_edges = set()

    for i in range(1, vertices_number + 1):
        for j in range(i + 1, vertices_number + 1):
            all_edges.add((i, j))

    return Graph(vertices_number, edges), Graph(vertices_number, all_edges - set(edges))


def print_solution(name: str, vertices_number: int, solution: [int], status: OptimizationStatus, iteration_number: int,clock_time: float, cpu_time: float) -> None:
    print("---", name, "---", "\n")
    print("Number of chosen vertices:", vertices_number)
    print("Found solution:", solution)
    print("Solution status:", status.name)
    print("Number of iterations:", iteration_number)
    print("Clock time:", clock_time)
    print("CPU time:", cpu_time, "\n\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Too few arguments (file_path, N)")
        exit(0)

    graph, complement_graph = parse_graph(sys.argv[1])
    n = int(sys.argv[2])

    solution_1 = graph.greedy_algorithm()

    tabu_solution = graph.tabu_search(solution_1, 500, 5)

    #
    # #complement_solution_1 = complement_graph.greedy_algorithm()
    solution_2, status, iteration_count, clock, cpu = graph.local_optimization(n)
    # #complement_solution_2, status_, iteration_count_, clock_, cpu_ = complement_graph.local_optimization(n)
    # solution_3, status_3, iteration_count_3, clock_3, cpu_3 = graph.local_optimization(n,majDegree=True)
    # solution_4, status_4, iteration_count_4, clock_4, cpu_4 = graph.local_optimization(n,orderRandom=True)
    # solution_5, status_5, iteration_count_5, clock_5, cpu_5 = graph.local_optimization(n,orderMix=True)
    #
    #
    # solRandom=[]
    # solMix=[]
    # for  i in range(30):
    #     solution_6, status_6, iteration_count_6, clock_6, cpu_6 = graph.local_optimization(n,orderRandom=True)
    #     solution_7, status_7, iteration_count_7, clock_7, cpu_7 = graph.local_optimization(n,orderMix=True)
    #     solRandom.append(len(solution_6))
    #     solMix.append(len(solution_7))
    #
    print_solution("Greedy algorithm", len(solution_1), [i + 1 for i in solution_1], OptimizationStatus.FEASIBLE, 1,None, None)
    # #print_solution("Complement greedy algorithm", len(complement_solution_1), [i + 1 for i in complement_solution_1],OptimizationStatus.FEASIBLE, 1, None, None)
    print_solution("Local optimization", len(solution_2), [i + 1 for i in solution_2], status, iteration_count, clock,cpu)
    # #print_solution("Complement local optimization", len(complement_solution_2), [i + 1 for i in complement_solution_2], status_, iteration_count_, clock_, cpu_)
    # print_solution("Local optimization avec maj degree", len(solution_3), [i + 1 for i in solution_3], status_3, iteration_count_3, clock_3,cpu_3)
    # print_solution("Local optimization avec ordre de parcours random", len(solution_4), [i + 1 for i in solution_4], status_4, iteration_count_4, clock_4,cpu_4)
    # print_solution("Local optimization avec ordre mix randoom / degree", len(solution_5), [i + 1 for i in solution_5], status_5, iteration_count_5, clock_5,cpu_5)
    # print("Random 30 iter: ",solRandom)
    # print("Mix 30 iter: ",solMix)

    print([i + 1 for i in tabu_solution])

    print(graph.verif_stable(solution_1))
    print(graph.verif_stable(solution_2))
    print(graph.verif_stable(tabu_solution))
