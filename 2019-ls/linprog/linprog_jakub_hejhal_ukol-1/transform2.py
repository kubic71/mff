import os
import sys

input_data = sys.stdin.readlines()

# linear program for glpsol
_, _, n_nodes, n_edges = input_data[0].strip().split()
n_nodes, n_edges = int(n_nodes), int(n_edges.replace(":", ""))


# edges[i] = (u, v, weight)
edges = [line.strip().replace("-->", " ").replace("(", " ").replace(")", " ").strip().split() for line in input_data[1:]]


# print("param N := {};".format(n_nodes))
print("set Edges := (0..{});".format(n_edges - 1))
print("var e_{i in Edges}, >= 0, <= 1, integer;")
print("var min_val;")
print("maximize obj: min_val;")

print("m: min_val <= ", end="")
print(" + ".join(["e_[{}]*{}".format(i,edge[2]) for i, edge in enumerate(edges)]), ";")


constraint_num = 0
for i1, edge1 in enumerate(edges):
    for i2, edge2 in enumerate(edges):
        if edge1[1] != edge2[0]:
            continue
        for i3, edge3 in enumerate(edges):
            if edge2[1] != edge3[0]:
                continue

            # neni treba checkovat jestli edge3[0] == edge1[0], protoze graf neobsahuje 2-cykly
            if edge3[1] == edge1[0]:
                # 3-cycle found
                print("c{}: e_[{}] + e_[{}] + e_[{}] <= 2".format(constraint_num, i1, i2, i3), ";")
                constraint_num += 1

            else:
                for i4, edge4 in enumerate(edges):
                    if edge3[1] == edge4[0] and edge4[1] == edge1[0]:
                        # 4-cycle found
                        print("c{}: e_[{}] + e_[{}] + e_[{}] + e_[{}] <= 3".format(constraint_num, i1, i2, i3, i4), ";")
                        constraint_num += 1


print("var removed_edges_weight;")
print("r1: removed_edges_weight = ", end="")
print(" + ".join(["(1 - e_[{}])*{}".format(i, edge[2]) for i, edge in enumerate(edges)]), end="")
print(";")

print("solve;")
print('printf "#OUTPUT: %d\\n", removed_edges_weight;')

for i, edge in enumerate(edges):
    print('printf (if e_[{}] < 1 then "{}\\n" else "");'.format(i, edge[0] + " --> " + edge[1]))

print('printf "#OUTPUT END\\n";')
print("end;")
