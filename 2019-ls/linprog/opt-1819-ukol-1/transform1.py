import os
import sys

input_data = sys.stdin.readlines()

# linear program for glpsol
_, nodes, edges = input_data[0].strip().split()
nodes, edges = int(nodes), int(edges.replace(":", ""))

print("param N := {};".format(nodes))
print("set Vertices := (0..{});".format(nodes-1))
print("var v_{i in Vertices}, >= 0;")
print("var max_val;")
print("minimize obj: max_val;")


for i in range(nodes):
    print("m{}: v_[{}] <= max_val;".format(i,i))

# add edges constraints
for i, line in enumerate(input_data[1:]):
    u, _, v = line.strip().split()
    u, v = int(u), int(v)
    print("p{}: ".format(i) + "v_[{}] - v_[{}] >= 1;".format(v, u))


print("""solve;
printf "#OUTPUT: %d\\n", max_val;
printf{i in Vertices} "v_%d: %d\\n", i, v_[i];
printf "#OUTPUT END\\n";
end;""")
