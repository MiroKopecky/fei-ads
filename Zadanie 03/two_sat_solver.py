__author__ = 'Matúš Pohančenik'
__credits__ = ['https://bit.ly/3eO2q18', 'https://bit.ly/3vXHKuJ',
               'https://bit.ly/33rXxWi']

import sys
from collections import defaultdict


class Graph:
    """
    A class that represents graph.

    Attributes:
       V : number of vertices
       edges: edges
    """

    def __init__(self, vertices):
        """
        Constructs all the necessary attributes for graph object
        """
        self.V = vertices  # number of vertices
        self.edges = defaultdict(set)  # default dictionary to store graph

    def add_edge(self, u, v):
        self.edges[u].add(v)


def load_formula_from_file(file_name: str):
    """
    Function parses the input file.

    :param file_name: file name
    """
    with open(file_name, 'r') as file:
        # number of boolean variables, number of clauses in the formula
        n_var, n_clauses = [int(s) for s in file.readline().split()]
        clauses = list()  # list of individual clauses
        formula = list()  # representation of the whole formula in CNF

        for line in file.readlines():
            clause = [int(x) for x in line.split()]
            if len(clause) == 3:
                formula.append(build_formula(clause[0], clause[1]))
                clauses.append(prepare_clauses(clause[0], clause[1]))
            elif len(clause) == 2:
                formula.append(build_formula(clause[0], clause[0]))
                clauses.append(prepare_clauses(clause[0], clause[0]))
            else:
                raise Exception(f'Wrong clause format: {clause}')

    return n_var, n_clauses, clauses, (" ∧ ".join(formula))


def build_formula(l1: int, l2: int) -> str:
    """
    Function creates CNF representation of the formula.

    :param l1: literal  1
    :param l2: literal  2
    """
    if l1 == l2:
        return f"({'x' + str(l1) if (l1 > 0) else '¬x' + str(-1 * l1)})"
    else:
        return f"({'x' + str(l1) if (l1 > 0) else '¬x' + str(-1 * l1)} v" \
               f" {'x' + str(l2) if (l2 > 0) else '¬x' + str(-1 * l2)})"


def prepare_clauses(l1: int, l2: int) -> tuple[int, int]:
    """
    Function transforms literals to positive numbers
    1 -> 0, -1 -> 1, 2 -> 2, -2 -> 3...

    :param l1: literal  1
    :param l2: literal  2
    """
    return ((2 * l1 - 2) if (l1 > 0) else (-2 * l1 - 1),
            (2 * l2 - 2) if (l2 > 0) else (-2 * l2 - 1))


def build_graph(n_var: int, clauses: list):
    """
    Function constructs directed graph and inverse directed graph
    of implications (x ∨ y) ≡ (¬x => y) ∧ (¬y => x)
    (if one of the two variables is false, then the other one must be true)

    :param n_var: number of boolean variables
    :param clauses: clauses
    """
    graph = Graph(n_var * 2)  # directed graph
    inv_graph = Graph(n_var * 2)  # inverse directed graph

    # x ∨ y ≡ ¬x => y ∧ ¬y => x
    for l1, l2 in clauses:

        # ¬x => y
        if l1 % 2 == 0:
            # positive variable
            graph.add_edge(l1 + 1, l2)
            inv_graph.add_edge(l2, l1 + 1)
        else:
            # negative variable
            graph.add_edge(l1 - 1, l2)
            inv_graph.add_edge(l2, l1 - 1)

        # ¬y => x
        if l2 % 2 == 0:
            # positive variable
            graph.add_edge(l2 + 1, l1)
            inv_graph.add_edge(l1, l2 + 1)
        else:
            # negative variable
            graph.add_edge(l2 - 1, l1)
            inv_graph.add_edge(l1, l2 - 1)

    return graph, inv_graph


def fill_order(edges: defaultdict, visited: list, order: list, v: int):
    """
    Function does the first step of Kosaraju's Algorithm

    :param edges: graph
    :param visited: visited vertices
    :param order: finish time order of vertices
    :param v: vertex index
    """
    visited[v] = True
    for u in edges[v]:
        if not visited[u]:
            fill_order(edges, visited, order, u)
    order.append(v)


def process_order(edges: defaultdict, comp: list, v: int, counter: int):
    """
    Function does the second step of Kosaraju's Algorithm

    :param edges: graph
    :param comp: components
    :param v: vertex index
    :param counter: counter
    """
    comp[v] = counter
    for u in edges[v]:
        if comp[u] == -1:
            process_order(edges, comp, u, counter)


def scc(graph: Graph, inv_graph: Graph):
    """
    Function finds strongly connected components

    :param graph: directed graph
    :param inv_graph: inverse directed graph
    """
    counter = 1
    order = []
    visited = [False] * graph.V
    components = [-1] * inv_graph.V  # SCC

    # traversing the original graph
    for v in range(graph.V):
        if not visited[v]:
            fill_order(graph.edges, visited, order, v)

    # traversing the inverse graph
    while order:
        v = order.pop()
        if components[v] == -1:
            process_order(inv_graph.edges, components, v, counter)
            counter += 1

    return components


def is_formula_satisfiable(components: list):
    """
    Function determines if the formula is satisfiable

    if x is reachable from ¬x, and ¬x is reachable from x,
    then the problem has no solution

    :param components: components
    """
    satisfiability = True
    for l1, l2 in zip(components[0::2], components[1::2]):
        if l1 == l2:
            satisfiability = False
            break

    print("SPLNITEĽNÁ") if satisfiability else print("NESPLNITEĽNÁ")
    return satisfiability


def get_bool_values(components: list):
    """
    Function assigns truth values to variables

     if comp[x] > comp[¬x] we assign x with true and false otherwise

    :param components: components
    """
    assignment = []
    for l1, l2 in zip(components[0::2], components[1::2]):
        if l1 > l2:
            print("PRAVDA")
            assignment.append(True)
        else:
            print("NEPRAVDA")
            assignment.append(False)

    return assignment


def print_formula(clauses: list, bool_values: list):
    """
    Function prints the formula with assigned truth values

    :param clauses: clauses
    :param bool_values: boolean values
    """
    # formula = list()
    bool_formula = list()
    assignment = dict()

    for i, bool_value in enumerate(bool_values, 1):
        i = 2 * i - 2
        assignment[i] = bool_value
        assignment[i + 1] = not bool_value

    for l1, l2 in clauses:
        if l1 == l2:
            bool_formula.append(f"({assignment[l1]})")
            # formula.append("({})".format(
            #     'x' + str((l1 + 2) // 2) if (l1 % 2 == 0) else '¬x' + str(
            #         (l1 + 1) // 2)))

        else:
            bool_formula.append(f"({assignment[l1]} ∨ {assignment[l2]})")
            # formula.append("({} ∨ {})".format(
            #     'x' + str((l1 + 2) // 2) if (l1 % 2 == 0) else '¬x' + str(
            #         (l1 + 1) // 2),
            #     'x' + str((l2 + 2) // 2) if (l2 % 2 == 0) else '¬x' + str(
            #         (l2 + 1) // 2)))

    # print(f'Formula: {" ∧ ".join(formula)}')
    print(f'Formula: {" ∧ ".join(bool_formula)}')


def main():
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = input("Zadajte názov vstupného súboru: ")

    n_var, n_clauses, clauses, formula = load_formula_from_file(file_name)
    print(f'Formula: {formula}')
    graph, inv_graph = build_graph(n_var, clauses)
    components = scc(graph, inv_graph)

    if is_formula_satisfiable(components):
        bool_values = get_bool_values(components)
        print_formula(clauses, bool_values)


if __name__ == '__main__':
    main()
