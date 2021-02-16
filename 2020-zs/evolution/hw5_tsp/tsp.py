import functools
import math
import numpy as np
import random

import utils
import matplotlib.pyplot as plt



# reads the input set of values of objects
def read_locations(filename):
    locations = []
    with open(filename) as f:
        for l in f.readlines():
            tokens = l.split(' ')
            locations.append((float(tokens[0]), float(tokens[1])))
    return locations
    
cities = read_locations('inputs/tsp_std.in')

@functools.lru_cache(maxsize=None) # this enables caching of the values
def distance(loc1, loc2):
    # based on https://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [loc1[1], loc1[0], loc2[1], loc2[0]])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371.01 * c
    return km


def edge_distance(index1, index2):
    # inter-city distance given by indeces into city array
    return distance(cities[index1], cities[index2])


# creates the population using the create individual function
def create_pop(pop_size, create_individual):
    return [create_individual() for _ in range(pop_size)]

# the tournament selection
def tournament_selection(pop, fits, k):
    selected = []
    for _ in range(k):
        p1 = random.randrange(0, len(pop))
        p2 = random.randrange(0, len(pop))
        if fits[p1] > fits[p2]:
            selected.append(pop[p1][:])
        else:
            selected.append(pop[p2][:])

    return selected

### Various crossover implementations

# implements the order crossover of two individuals
def order_cross(p1, p2):
    point1 = random.randrange(1, len(p1))
    point2 = random.randrange(1, len(p1))
    start = min(point1, point2)
    end = max(point1, point2)

    # swap the middle parts
    o1mid = p2[start:end]
    o2mid = p1[start:end]

    # take the rest of the values and remove those already used
    restp1 = [c for c in p1[end:] + p1[:end] if c not in o1mid]
    restp2 = [c for c in p2[end:] + p2[:end] if c not in o2mid]

    o1 = restp1[-start:] + o1mid + restp1[:-start]
    o2 = restp2[-start:] + o2mid + restp2[:-start]

    return o1, o2

def cycle_cross(x1, x2):
    n_cities = len(x1)
    # y1, y2 = np.ones((n_cities,))*(-1), np.ones((n_cities,))*(-1)
    y1, y2 = [-1] * n_cities, [-1] * n_cities

    i = 0
    while True:
        j = x1.index(x2[i])

        y1[j] = x1[j]
        y2[j] = x2[j]
        i = j

        if x2[i] in y1:
            break

    for i in range(n_cities):
        if y1[i] == -1:
            y1[i] = x2[i]

        if y2[i] == -1:
            y2[i] = x1[i]

    return y1, y2

def pmx_cross(x1, x2):
    n_cities = len(x1)
    s1, s2 = sorted(list(np.random.choice(range(n_cities + 1), size=2, replace=False)))    # n + 1 possible split points

    y1, y2 = [-1] * n_cities, [-1] * n_cities


    for i in range(s1, s2):
        # swap middle parts
        y1[i] = x2[i]
        y2[i] = x1[i]


    map_x1_x2 = dict(zip(x1[s1:s2], x2[s1:s2]))
    map_x2_x1 = dict(zip(x2[s1:s2], x1[s1:s2]))


    # fill offspring's i-th position
    def fill(y, x, mapping, i):
        candidate = x[i]
        while True:
            if candidate not in y:
                y[i] = candidate
                return
            
            candidate = mapping[candidate]

    for i in list(range(0, s1)) + list(range(s2, n_cities)):
        fill(y1, x1, map_x2_x1, i)
        fill(y2, x2, map_x1_x2, i)

    return y1, y2

        
def edge_recomb_cross_one(p1, p2):
    # This crossover is order of magnitude slower than other crossovers (PMX, NWOX ...)


    n_cities = len(p1)
    edges = {}
    for c in p1:
        edges[c] = set()

    def add_edges(p):
        for i in range(n_cities):
            i1, i2, i3 = (i-1) % n_cities, i % n_cities, (i+1) % n_cities

            edges[p[i2]].add(p[i3]) # forward edge
            edges[p[i2]].add(p[i1]) # backward edge

    def remove_node(node):
        for key in edges:
            if node in edges[key]:
                edges[key].remove(node)

    add_edges(p1)
    add_edges(p2)

    y = []

    # starting node is the first node of random parent
    node = random.choice([p1, p2])[0]
    y.append(node)

    all_nodes = set(p1)

    while len(y) < n_cities:
        remove_node(node)

        if len(edges[node]) > 0:
            min_n = min([len(edges[c])  for c in edges[node]])
            candidates = [c for c in edges[node] if len(edges[c]) == min_n] 

            # choose randomly next node from next nodes with the same number of unused neighbours
            node = random.choice(candidates)
        
        else:
            # randomly choose some unused node
            node = random.choice(list(all_nodes - set(y)))
        y.append(node)

    return y

def edge_recomb_cross(p1, p2):
    # crossover operator is expected to produce 2 offsprings
    return edge_recomb_cross_one(p1, p2), edge_recomb_cross_one(p1, p2)


    


# implements the non-wrapping order crossover of two individuals
def nwox_cross(p1, p2):
    point1 = random.randrange(1, len(p1))
    point2 = random.randrange(1, len(p1))
    start = min(point1, point2)
    end = max(point1, point2)

    # swap the middle parts
    o1mid = p2[start:end]
    o2mid = p1[start:end]

    # take the rest of the values and remove those already used
    restp1 = [c for c in p1 if c not in o1mid]
    restp2 = [c for c in p2 if c not in o2mid]

    o1 = restp1[:start] + o1mid + restp1[start:]
    o2 = restp2[:start] + o2mid + restp2[start:]

    return o1, o2



# implements the swapping mutation of one individual
def swap_mutate(p, max_len):
    source = random.randrange(1, len(p) - 1)
    dest = random.randrange(1, len(p))
    lenght = random.randrange(1, min(max_len, len(p) - source))

    o = p[:]
    move = p[source:source+lenght]
    o[source:source + lenght] = []
    if source < dest:
        dest = dest - lenght # we removed `lenght` items - need to recompute dest
    
    o[dest:dest] = move
    
    return o

def two_opt_mut(p, max_len):
    o = p[:]

    s1, s2 = sorted(list(np.random.choice(range(len(p)), size=2, replace=False)))  

    e1 = edge_distance(p[s1], p[s1 + 1])
    e2 = edge_distance(p[s2], p[(s2 + 1) % len(p)])

    e3 = edge_distance(p[s1], p[s2])
    e4 = edge_distance(p[s1 + 1], p[(s2 + 1) % len(p)])

    if e3 + e4  < e1 + e2:
        o[s1+1:s2] = reversed(o[s1+1:s2])
    
    return o


def slide_mut(p, max_len):
    s1, s2 = sorted(list(np.random.choice(range(len(p)), size=2, replace=False)))  

    # slide in s1 after s2 as follows:
    # a, b, s1, c, d, e, s2, f, g
    #           |
    #           V
    # a, b, c, d, e, s2, s1, f, g

    o = p[:s1] + p[s1+1:s2+1] + [p[s1]] + p[s2+1:]
    
    return o


def hybridCrossoverRandom(cross_set, weights):
    weights = np.array(weights) / sum(weights)

    def xover_func(x1, x2):
        xover = np.random.choice(cross_set, p=weights)
        return xover(x1, x2)
    
    return xover_func

def hybridCrossoverBest(cross_set):

    def xover_func(x1, x2):
        best = float("-inf")
        for cross in cross_set:
            o1, o2 = cross(x1, x2)
            b = max(fitness(o1, cities).fitness, fitness(o2, cities).fitness)
            if b > best:
                y1, y2 = o1, o2
                best = b
        return y1, y2
    
    return xover_func

def hybridMutationRandom(mutate_set, weights):
    weights = np.array(weights) / sum(weights)
    
    def mut_func(p, max_len):
        mut = np.random.choice(mutate_set, p=weights)
        return mut(p, max_len)

    return mut_func

def hybridMutationBest(mutate_set):

    def mut_func(p, max_len):
        best = float("-inf")
        for mut in mutate_set:
            o = mut(p, max_len)
            fit = fitness(o, cities).fitness
            if fit > best:
                y = o
                best = fit
            
        return y
    
    return mut_func


## Various initialization strategies

# creates the individual (random permutation)
def create_random_perm(ind_len):
    ind = list(range(ind_len))
    random.shuffle(ind)
    return ind
    

def generate_path_nn(ind_len):
    remaining = set([j for j in range(len(cities))])
    start = random.randrange(0, len(cities))
    path = [start]
    remaining.remove(start)

    while len(remaining) > 0:
        current = path[-1]
        distances = sorted([(r, edge_distance(current, r)) for r in remaining], key=lambda x: x[1])
        city_indeces = [d[0] for d in distances]
        weights = 1 / np.array([d[1] for d in distances])

        next_city = np.random.choice(city_indeces, p=weights/sum(weights))
        path.append(next_city)
        remaining.remove(next_city)

    return path


import mst
# print("Generating MST")
mst_graph = mst.mst(len(cities), edge_distance)
# print("MST generated")

def mst_heuristic(ind_len):
    # generate individual by random walk over minimum spanning tree of the cities
    start = random.randrange(0, ind_len)
    path = [start]

    def dfs(current):
        neighbours = mst_graph[current][:]
        random.shuffle(neighbours)
        for n in neighbours:
            if n not in path:
                path.append(n)
                dfs(n)

    dfs(start)

    return path
                




def hybrid_ind(gen_funcs, weights):
    weights = np.array(weights) / sum(weights)
    
    def gen_func(ind_len):
        f = np.random.choice(gen_funcs, p=weights)
        return f(ind_len)

    return gen_func 



# applies a list of genetic operators (functions with 1 argument - population) 
# to the population


# egde-recombination takes too long, compute it in parallel on small chunks of population

def mate(pop, operators):
    for o in operators:
        pop = o(pop)

    return pop


# applies the cross function (implementing the crossover of two individuals)
# to the whole population (with probability cx_prob)
def crossover(pop, cross, cx_prob):
    off = []
    for p1, p2 in zip(pop[0::2], pop[1::2]):
        if random.random() < cx_prob:
            o1, o2 = cross(p1, p2)
        else:
            o1, o2 = p1[:], p2[:]
        off.append(o1)
        off.append(o2)
    return off

# applies the mutate function (implementing the mutation of a single individual)
# to the whole population with probability mut_prob)
def mutation(pop, mutate, mut_prob):
    return [mutate(p) if random.random() < mut_prob else p[:] for p in pop]

# implements the evolutionary algorithm
# arguments:
#   pop_size  - the initial population
#   max_gen   - maximum number of generation
#   fitness   - fitness function (takes individual as argument and returns 
#               FitObjPair)
#   operators - list of genetic operators (functions with one arguments - 
#               population; returning a population)
#   mate_sel  - mating selection (funtion with three arguments - population, 
#               fitness values, number of individuals to select; returning the 
#               selected population)
#   map_fn    - function to use to map fitness evaluation over the whole 
#               population (default `map`)
#   log       - a utils.Log structure to log the evolution run
def evolutionary_algorithm(pop, pop_size, max_gen, fitness, operators, mate_sel, *, map_fn=map, log=None, progress_callback=None):
    evals = 0
    for G in range(max_gen):
        fits_objs = list(map_fn(fitness, pop))
        evals += len(pop)
        if log:
            log.add_gen(fits_objs, evals)
        fits = [f.fitness for f in fits_objs]
        objs = [f.objective for f in fits_objs]

        mating_pool = mate_sel(pop, fits, pop_size)
        offspring = mate(mating_pool, operators)

        best = max(list(zip(fits, pop)), key = lambda x: x[0])
        pop = offspring[:-1] + [best[1]]


        if progress_callback is not None:
            progress_callback(-best[0], evals)

    return pop


# the fitness function
def fitness(ind, cities):

    
    # quickly check that ind is a permutation
    num_cities = len(cities)
    assert len(ind) == num_cities
    assert sum(ind) == num_cities*(num_cities - 1)//2
    dist = 0
    for a, b in zip(ind, ind[1:]):
        dist += distance(cities[a], cities[b])
    
    dist += distance(cities[ind[-1]], cities[ind[0]])

    return utils.FitObjPair(fitness=-dist, 
                            objective=dist)


OUT_DIR = 'tsp' # output directory for logs

def run_experiment(exp_id='default', data_input='inputs/tsp_std.in', repeats=10, mut_max_len=10, mut_prob=0.2, cx_prob=0.8, max_gen=500, pop_size=100, fitness=fitness,  create_ind=None, cross=order_cross, mutate=swap_mutate,  print_frequency=5, progress_callback=None):
    # read the locations from input
    locations = read_locations(data_input)

    # use `functool.partial` to create fix some arguments of the functions 
    # and create functions with required signatures
    cr_ind = functools.partial(create_ind, ind_len=len(locations))


    globals()['cities'] = locations
    fit = functools.partial(fitness, cities=locations)
    xover = functools.partial(crossover, cross=cross, cx_prob=cx_prob)
    mut = functools.partial(mutation, mut_prob=mut_prob, 
                            mutate=functools.partial(mutate, max_len=mut_max_len))


    # run the algorithm `REPEATS` times and remember the best solutions from 
    # last generations
    best_inds = []
    best_objective = 100000000
    for run in range(repeats):
        # initialize the log structure
        log = utils.Log(OUT_DIR, exp_id, run, 
                        write_immediately=True, print_frequency=print_frequency)
        # create population
        pop = create_pop(pop_size, cr_ind)
        # run evolution - notice we use the pool.map as the map_fn
        pop = evolutionary_algorithm(pop, pop_size, max_gen, fit, [xover, mut], tournament_selection, map_fn=map, log=log, progress_callback=progress_callback)
        # remember the best individual from last generation, save it to file
        bi = max(pop, key=fit)
        best_objective = min(best_objective, fit(bi).objective)
        best_inds.append(bi)

        best_template = '{individual}'
        with open('resources/kmltemplate.kml') as f:
            best_template = f.read()

        with open(f'{OUT_DIR}/{exp_id}_{run}.best', 'w') as f:
            f.write(str(bi))

        with open(f'{OUT_DIR}/{exp_id}_{run}.best.kml', 'w') as f:
            bi_kml = [f'{locations[i][1]},{locations[i][0]},5000' for i in bi]
            bi_kml.append(f'{locations[bi[0]][1]},{locations[bi[0]][0]},5000')
            f.write(best_template.format(individual='\n'.join(bi_kml)))
        
        # if we used write_immediately = False, we would need to save the 
        # files now
        # log.write_files()

    # print an overview of the best individuals from each run
    for i, bi in enumerate(best_inds):
        print(f'Run {i}: difference = {fit(bi).objective}')

    # write summary logs for the whole experiment
    utils.summarize_experiment(OUT_DIR, exp_id)

    return best_objective


    # you can also plot mutiple experiments at the same time using 
    # utils.plot_experiments, e.g. if you have two experiments 'default' and 
    # 'tuned' both in the 'partition' directory, you can call
    # utils.plot_experiments('partition', ['default', 'tuned'], 
    #                        rename_dict={'default': 'Default setting'})
    # the rename_dict can be used to make reasonable entries in the legend - 
    # experiments that are not in the dict use their id (in this case, the 
    # legend entries would be 'Default settings' and 'tuned') 


def plot_experiments(*exp_names, transform_map=lambda x: x - 150000, ylim=[10000, 150000]):
    plt.figure(figsize=(12,8))
    plt.yscale("log")


    # settings specific for tsp_std.in input
    if ylim is not None:
        plt.ylim(ylim)

    utils.plot_experiments(OUT_DIR, exp_names, transform_map=transform_map)
    plt.show()