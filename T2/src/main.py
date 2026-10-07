"""
Fox And Names - Codeforces 510C
https://codeforces.com/problemset/problem/510/C

Execução:  python3 src/main.py < entrada.txt

As classes Node, LinkIterator, Bag, Digraph, DirectedCycle, DepthFirstOrder e
Topological são cópias das implementações de referência de algs4-py, reunidas
em um único arquivo porque o Codeforces aceita apenas um arquivo por submissão.
As alterações em relação à referência estão descritas em acompanhamento/marco-4.md.
"""

import sys
from collections import deque


# --- algs4/utils/linklist.py (sem alterações) ---

class Node:

    def __init__(self, item, next_node):
        self.item = item
        self.next = next_node


class LinkIterator:

    def __init__(self, current):
        self.current = current

    def __next__(self):
        if self.current is None:
            raise StopIteration()
        else:
            item = self.current.item
            self.current = self.current.next
            return item


# --- algs4/bag.py (removidos: __str__ e o bloco __main__) ---

class Bag:

    def __init__(self):
        self.first = None
        self.n = 0

    def __iter__(self):
        return LinkIterator(self.first)

    def size(self):
        return self.n

    def is_empty(self):
        return self.first is None

    def add(self, item):
        oldfirst = self.first
        self.first = Node(item, oldfirst)
        self.n += 1


# --- algs4/digraph.py (removidos: leitura por arquivo, __str__, degree,
#     max_degree, number_of_self_loops, reverse e o bloco __main__) ---

class Digraph:

    def __init__(self, v=0):
        self.V = v
        self.E = 0
        self.adj = [Bag() for _ in range(self.V)]

    def add_edge(self, v, w):
        v, w = int(v), int(w)
        self.adj[v].add(w)
        self.E += 1


# --- algs4/directed_cycle.py (removido: o bloco __main__) ---

class DirectedCycle:

    def __init__(self, G):
        self._marked = [False for _ in range(G.V)]
        self.edge_to = [False for _ in range(G.V)]
        self.on_stack = [False for _ in range(G.V)]
        self.cycle = None
        for v in range(G.V):
            if not self._marked[v]:
                self.dfs(G, v)

    def dfs(self, G, v):
        self._marked[v] = True
        self.on_stack[v] = True

        for w in G.adj[v]:
            if self.has_cycle():
                return
            if not self._marked[w]:
                self.edge_to[w] = v
                self.dfs(G, w)
            elif self.on_stack[w]:
                cycle = []
                x = v
                while x != w:
                    cycle.append(x)
                    x = self.edge_to[x]
                cycle.append(w)
                cycle.append(v)
                self.cycle = list(reversed(cycle))
        self.on_stack[v] = False

    def marked(self, v):
        return self._marked[v]

    def has_cycle(self):
        return self.cycle is not None


# --- algs4/depth_first_order.py (removido: o bloco __main__) ---

class DepthFirstOrder:

    def __init__(self, G):
        self.marked = [False for _ in range(G.V)]
        self.pre = deque()
        self.post = deque()
        for w in range(G.V):
            if not self.marked[w]:
                self.dfs(G, w)

    def dfs(self, G, v):
        self.pre.append(v)
        self.marked[v] = True

        for w in G.adj[v]:
            if not self.marked[w]:
                self.dfs(G, w)
        self.post.append(v)

    def reverse_post(self):
        return reversed(self.post)

    def reversePost(self):
        return self.reverse_post()


# --- algs4/topological.py (removidos: import de SymbolDigraph e o bloco __main__) ---

class Topological:
    def __init__(self, g):
        self.order = None
        finder = DirectedCycle(g)
        if not finder.has_cycle():
            dfs = DepthFirstOrder(g)
            self.order = dfs.reversePost()

    def has_order(self):
        return self.order != None


# --- Código específico do problema ---

LETRAS = 26


def indice(c):
    return ord(c) - ord('a')


def construir_grafo(nomes):
    """Cria o dígrafo de precedência das letras a partir de nomes consecutivos.

    Retorna None quando um nome aparece antes de um prefixo seu, caso que
    nenhuma ordem do alfabeto resolve.
    """
    g = Digraph(LETRAS)
    existe = [[False] * LETRAS for _ in range(LETRAS)]  # evita arestas repetidas

    for s, t in zip(nomes, nomes[1:]):
        for x, y in zip(s, t):
            if x != y:
                u, v = indice(x), indice(y)
                if not existe[u][v]:
                    existe[u][v] = True
                    g.add_edge(u, v)
                break
        else:
            # nenhuma posição diferente: um nome é prefixo do outro
            if len(s) > len(t):
                return None
    return g


def resolver(nomes):
    g = construir_grafo(nomes)
    if g is None:
        return "Impossible"

    topological = Topological(g)
    if not topological.has_order():
        return "Impossible"

    return "".join(chr(ord('a') + v) for v in topological.order)


def main():
    dados = sys.stdin.read().split()
    n = int(dados[0])
    nomes = dados[1:1 + n]
    print(resolver(nomes))


if __name__ == '__main__':
    main()
