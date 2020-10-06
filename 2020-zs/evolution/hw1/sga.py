import random
import pprint

import numpy as np
import utils

IND_LEN = 25

# creates a single individual of lenght `lenght`
def create_ind(length):
    return [random.randint(0, 1) for _ in range(length)]

# creates a population of `size` individuals
def create_population(size):
    return [create_ind(IND_LEN) for _ in range(size)]

# tournament selection
# def selection(pop, fits):
#     selected = []
#     for _ in range(len(pop)):
#         i1, i2 = random.randrange(0, len(pop)), random.randrange(0, len(pop))
#         if fits[i1] > fits[i2]:
#             selected.append(pop[i1])
#         else: 
#             selected.append(pop[i2])
#     return selected

# roulette wheel selection
def selection(pop, fits):
    return random.choices(pop, fits, k=len(pop))

# one point crossover
def cross(p1, p2):
    point = random.randint(0, len(p1))
    o1 = p1[:point] + p2[point:]
    o2 = p2[:point] + p1[point:]
    return o1, o2

# applies crossover to all individuals
def crossover(pop, cx_prob):
    off = []
    for p1, p2 in zip(pop[0::2], pop[1::2]):
        o1, o2 = p1[:], p2[:]
        if random.random() < cx_prob:
            o1, o2 = cross(p1[:], p2[:])
        off.append(o1)
        off.append(o2)
    return off

# bit-flip mutation
def mutate(p, mut_prob, mut_flip_prob):
    if random.random() < mut_prob:
        return [1 - i if random.random() < mut_flip_prob else i for i in p]
    return p[:]
    
# applies mutation to the whole population
def mutation(pop, mut_prob, mut_flip_prob):
    return list(map(lambda p: mutate(p, mut_prob, mut_flip_prob), pop))

# applies crossover and mutation
def operators(pop, mut_prob, mut_flip_prob, cx_prob):
    pop1 = crossover(pop, cx_prob)
    return mutation(pop1, mut_prob, mut_flip_prob)


# implements the whole EA
def evolutionary_algorithm(fitness_fn, objective_fn, logger, 
    pop_size = 100,
    cx_prob = 0.8,
    mut_prob = 0.05,
    mut_flip_prob = 0.1,
    generations = 100):

    pop = create_population(pop_size)
    for G in range(generations):
        fit_obj = list(map(lambda pair: utils.FitObjPair(pair[0], pair[1]),  zip(map(fitness_fn, pop), map(objective_fn, pop))))
        
        evals = G * pop_size
        logger.add_gen(fit_obj, evals)
        
        
        # log.append((G, max(fits), sum(fits)/100, G*POP_SIZE))
        #print(G, sum(fits), max(fits)) # prints fitness to console
        mating_pool = selection(pop, [f.fitness for f in fit_obj])
        offspring = operators(mating_pool, mut_prob, mut_flip_prob, cx_prob)
        #pop = offspring[:-1]+[max(pop, key=fitness)] #SGA + elitism
        pop = offspring[:] #SGA
    
    logger.write_files()
    return pop

    

# for i in range():
#     random.seed(i)
#     pop,log = evolutionary_algorithm(fitness)
#     logs.append(log)
# fits = list(map(fitness, pop))
# # pprint.pprint(list(zip(fits, pop)))
# # print(sum(fits), max(fits))
# # pprint.pprint(log)
# 
# # extract fitness evaluations and best fitnesses from logs
# evals = []
# best_fit = []
# for log in logs:
#     evals.append([l[3] for l in log])
#     best_fit.append([l[1] for l in log])
# 
# evals = np.array(evals)
# best_fit = np.array(best_fit)
# 
# # plot the converegence graph and quartiles
# import matplotlib.pyplot as plt
# _, ax = plt.subplots() 
# 
# ax.plot(evals[0,:], np.median(best_fit, axis=0), label = "median")
# ax.fill_between(evals[0,:], np.percentile(best_fit, q=25, axis=0),
#   np.percentile(best_fit, q=75, axis=0), alpha = 0.2, label = "Interquartile range")
# 
# legend = ax.legend(loc="upper center", shadow = True, fontsize = 'large')
# 
# 
# plt.show()