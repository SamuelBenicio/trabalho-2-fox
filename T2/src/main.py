"""
Fox And Names - Codeforces 510C
https://codeforces.com/problemset/problem/510/C

Usage:  python3 src/main.py < dados/entrada.txt

The classes Node, LinkIterator, Bag, Digraph, DirectedCycle, DepthFirstOrder and
Topological are copies of the algs4-py reference implementations, gathered in a
single file because Codeforces accepts only one file per submission.
The changes relative to the reference are described in acompanhamento/marco-4.md.
"""

import sys
from collections import deque


# --- algs4/utils/linklist.py (unchanged) ---

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


# --- algs4/bag.py (removed: __str__ and the __main__ block) ---

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


# --- algs4/digraph.py (removed: reading from file, __str__, degree,
#     max_degree, number_of_self_loops, reverse and the __main__ block;
#     added: has_edge) ---

class Digraph:

    def __init__(self, v=0):
        self.V = v
        self.E = 0
        self.adj = [Bag() for _ in range(self.V)]

    def add_edge(self, v, w):
        v, w = int(v), int(w)
        self.adj[v].add(w)
        self.E += 1

    def has_edge(self, v, w):
        return any(x == w for x in self.adj[v])


# --- algs4/directed_cycle.py (removed: the __main__ block) ---

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


# --- algs4/depth_first_order.py (removed: the __main__ block) ---

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


# --- algs4/topological.py (removed: SymbolDigraph import and the __main__ block) ---

class Topological:
    def __init__(self, g):
        self.order = None
        finder = DirectedCycle(g)
        if not finder.has_cycle():
            dfs = DepthFirstOrder(g)
            self.order = dfs.reversePost()

    def has_order(self):
        return self.order != None


# --- Problem-specific code ---

LETTERS = 26
IMPOSSIBLE = "Impossible"


class ImpossibleOrder(Exception):
    """No alphabet order makes the names sorted."""


def index(c):
    """Converts a letter to its vertex index: 'a' -> 0, ..., 'z' -> 25."""
    return ord(c) - ord('a')


def letter(v):
    """Converts a vertex index back to its letter: 0 -> 'a', ..., 25 -> 'z'."""
    return chr(ord('a') + v)


def build_graph(names):
    """Builds the letter precedence digraph from consecutive names.

    Raises ImpossibleOrder when a name appears before one of its prefixes,
    a case no alphabet order can fix.
    """
    graph = Digraph(LETTERS)

    for s, t in zip(names, names[1:]):
        for x, y in zip(s, t):
            if x != y:
                u, v = index(x), index(y)
                if not graph.has_edge(u, v):  # keeps the graph simple
                    graph.add_edge(u, v)
                break
        else:
            # no differing position: one name is a prefix of the other
            if len(s) > len(t):
                raise ImpossibleOrder()
    return graph


def topological_order(graph):
    """Returns a topological order of the graph.

    Raises ImpossibleOrder when the graph has a cycle (contradictory constraints).
    """
    topological = Topological(graph)
    if not topological.has_order():
        raise ImpossibleOrder()
    return topological.order


def restricted_letters(graph):
    """Marks the letters that appear in some edge."""
    restricted = [False] * LETTERS
    for v in range(LETTERS):
        for w in graph.adj[v]:
            restricted[v] = True
            restricted[w] = True
    return restricted


def solve(names):
    try:
        graph = build_graph(names)
        order = topological_order(graph)
    except ImpossibleOrder:
        return IMPOSSIBLE

    restricted = restricted_letters(graph)

    # First the restricted letters, in topological order (preserves the edges);
    # then the free letters, in alphabetical order (they have no constraints).
    alphabet = [letter(v) for v in order if restricted[v]]
    alphabet += [letter(v) for v in range(LETTERS) if not restricted[v]]
    return "".join(alphabet)


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    print(solve(names))


if __name__ == '__main__':
    main()
