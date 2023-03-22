import sys
import mip
import time
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

    def local_optimization(self, n: int) -> tuple[list[int], OptimizationStatus, int, float, float]:
        degrees = [len(self.adjacent_vertices[i]) for i in range(self.vertices_number)]
        order = sorted(range(self.vertices_number), key=lambda i: degrees[i])
        selected = []
        status = -1
        iterations_count = 0

        clock_start = 0
        clock_end = 0
        cpu_start = 0
        cpu_end = 0

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

            # Ajout des sommets sélectionnés dans la liste de sélection
            for i in range(len(candidates)):
                if float(x[i].x) > 0.9:
                    selected.append(candidates[i])
                    if len(selected) == n:
                        break

        return sorted(selected), status, iterations_count, clock_end - clock_start, cpu_end - cpu_start


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


def print_solution(name: str, vertices_number: int, solution: [int], status: OptimizationStatus, iteration_number: int,
                   clock_time: float, cpu_time: float) -> None:
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
    complement_solution_1 = complement_graph.greedy_algorithm()
    solution_2, status, iteration_count, clock, cpu = graph.local_optimization(n)
    complement_solution_2, status_, iteration_count_, clock_, cpu_ = complement_graph.local_optimization(n)

    print_solution("Greedy algorithm", len(solution_1), [i + 1 for i in solution_1], OptimizationStatus.FEASIBLE, 1,
                   None, None)
    print_solution("Complement greedy algorithm", len(complement_solution_1), [i + 1 for i in complement_solution_1],
                   OptimizationStatus.FEASIBLE, 1, None, None)
    print_solution("Local optimization", len(solution_2), [i + 1 for i in solution_2], status, iteration_count, clock,
                   cpu)
    print_solution("Local optimization", len(complement_solution_2), [i + 1 for i in complement_solution_2], status_,
                   iteration_count_, clock_, cpu_)

    # ok = set()
    # for i in sol2:
    #     for j in sol2:
    #         if j > i and j in graph.adjacent_vertices[i]:
    #             ok.add(i)
    # print(len(ok))
