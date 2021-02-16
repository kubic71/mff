class Node:
   def __init__(self, val):
       self.val = val
       self.parent = self
       self.size = 1

def find(node):
    if node.parent is not node:
        node.parent = find(node.parent)
        return node.parent
    else:
        return node
        

def union(x, y):
    x = find(x)
    y = find(y)
    if x is y:
        print("Union called on the same sets")
        return
    
    if x.size < y.size:
        x, y = y, x

    y.parent = x
    x.size = x.size + y.size


def mst(n, edge_distance):
    # kruskal
    vertices = [Node(i) for i in range(n)]

    edges = {}
    for x in range(n):
        for y in range(x + 1, n):
            d = edge_distance(x, y)
            edges[(x, y)] = d

    edges = sorted(edges.items(), key=lambda item: item[1])

    # return MST represented as a list of neighbours
    neighbours = [[] for i in range(n)]

    unions = 0
    for (x, y), d in edges:
        x, y = vertices[x], vertices[y]
        f1 = find(x)
        f2 = find(y)
        if f1 is f2:
            continue

        union(x, y)

        # add edge in the MST between the two components
        neighbours[x.val].append(y.val)
        neighbours[y.val].append(x.val)

        unions += 1
        if unions == n - 1:
            return neighbours



# Unit test

points = [(1, 1), (3, 2), (4, 2), (3, 3), (4,3), (1, 5), (2,5)]
def edge_dist(i1, i2):
    x1, y1 = points[i1]
    x2, y2 = points[i2]

    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

m = mst(7, edge_dist)
# print(m)











