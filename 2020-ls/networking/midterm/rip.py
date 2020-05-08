d = {("A", "B"): 10,
        ("A", "D"):10,
        ("B", "C"):50,
        ("D", "C"):5,
        ("C", "F"):8,
        ("C", "E"):10,
        ("D", "E"):3 }

nodes = "ABCDEF"

def symmetrize(d):
    new = {}

    for n in nodes:
        new[(n, n)]  = 0

    for a, b in d:
        new[(a,b)] = d[(a,b)]
        new[(b,a)] = d[(a,b)]

    return new



def dist_matrix(d):
    # return full matrix from dict 
    m = [[float("inf") if (a,b) not in d else d[(a,b)] for a in nodes] for b in nodes]
    return m


def print_m(m):
    print("\t" + "\t".join(nodes))

    for i, a in enumerate(nodes):
        print(a + "\t", end="")

        for j, b in enumerate(nodes):
            print(str(m[i][j]) + "\t", end="")
        print()


d = symmetrize(d)
print(d)

m = dist_matrix(d)
print_m(m)


def step(m):
    import copy
    new_m = copy.deepcopy(m)
    
    
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            for k, c in enumerate(nodes):
                new_m[i][j] = min(new_m[i][j], m[i][k] + m[k][j])

    return new_m

def iterate(m):
    i = 1
    while True:
        new_m = step(m)
        if new_m == m:
            break
        m = new_m

        print("\nIteration ", i)
        print_m(new_m)

        i += 1

    return m


m = iterate(m)


# Let's add node G

for a in nodes:
    m[nodes.index(a)].append(float("inf"))

nodes += "G"
m = m + [[float("inf") for i in range(len(nodes))]]


g_i = len(nodes) - 1
e_i = nodes.index("E")


m[g_i][g_i] = 0
m[e_i][g_i] = 14
m[g_i][e_i] = 14


print("\nAdded G node")
print_m(m)
iterate(m)


                
    
        

