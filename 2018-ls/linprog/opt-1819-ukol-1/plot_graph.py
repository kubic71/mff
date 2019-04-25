import argparse
import networkx as nx
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser()
parser.add_argument("--file", help="filename of graph to plot")
args = parser.parse_args()

with open('vstupy/' + args.file,'r') as f:
    output = f.read()

g = nx.DiGraph()

output = output.strip().split("\n")
_, nodes, edges = output[0].strip().split()
nodes, edges = int(nodes), int(edges.replace(":", ""))
print("Nodes:", nodes, ", Edges:", edges)
g.add_nodes_from(list(range(nodes)))
for line in output[1:]:
    line = line.split()
    u, v = line[0], line[2]
    g.add_edge(int(u), int(v))

nx.draw(g,with_labels=True, cmap = plt.get_cmap('jet'))
plt.draw()
plt.show()