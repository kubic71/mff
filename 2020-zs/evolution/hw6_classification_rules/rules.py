import utils
import math
import matplotlib.pyplot as plt
import copy
import csv
import functools
import random



from collections import namedtuple, defaultdict

import numpy as np

import utils

OUT_DIR = 'rules' # output directory for logs

# a rule is a list of conditions (one for each attribute) and the predicted class
Rule = namedtuple('Rule', ['conditions', 'cls', 'priority'])


# the following 3 classes implement simple conditions, the call method is used 
# to match the condition against a value
class LessThen:
    def __init__(self, lb, ub):
        threshold = random.random()
        self.params = np.array([threshold])
        self.lb = lb
        self.ub = ub

    def boundary(self):
        return (self.ub - self.lb)*self.params[0] + self.lb

    def __call__(self, value):
        return value <= self.boundary()
    
    def __str__(self):
        return " <= " + str(self.boundary())

class GreaterThen:

    def __init__(self, lb, ub):
        threshold = random.random()
        self.params = np.array([threshold])
        self.lb = lb
        self.ub = ub

    def boundary(self):
        return (self.ub - self.lb)*self.params[0] + self.lb

    def __call__(self, value):
        return value >= self.boundary()

    def __str__(self):
        return " >= " + str(self.boundary())

class Any:

    def __init__(self, lb, ub):
        self.params = np.array([])
    
    def __call__(self, value):
        return True

    def __str__(self):
        return " * "


# creates the individual - list of rules
def create_ind(max_rules, num_attrs, num_classes, lb, ub, cond_dist, priority, most_frequent_cls):
    rules = []
    ind_len = random.randrange(1, max_rules)
    for j in range(ind_len):
        conditions = []
        conds = list(map(lambda x: x[0], cond_dist))
        weights = list(map(lambda x: x[1], cond_dist))

        for i in range(num_attrs):
            cond = np.random.choice(conds, p=weights)
            conditions.append(cond(lb[i], ub[i]))
    
        p = 1
        cls = most_frequent_cls
        if priority:
            p = random.random()*2 - 1

            if p < 0:
                cls = random.randrange(0, num_classes)
        
        if cls == -1:
            most_frequent_cls = random.randrange(0, num_classes)

        rules.append(Rule(conditions=conditions, cls=cls, priority=p))

    return rules


# creates the population using the create individual function
def create_pop(pop_size, create_individual):
    return [create_individual() for _ in range(pop_size)]

# uses an individual to predict a single instance - the rules in the individual
# vote for the final class
def classify_instance(ind, attrs):
    votes = defaultdict(int)
    for rule in ind:
        if all([cond(a) for cond, a in zip(rule.conditions, attrs)]):
            votes[rule.cls] += rule.priority
    
    best_class = None
    best_votes = -10000
    for k, v in votes.items():
        if v > best_votes:
            best_votes = v
            best_class = k

    if best_class == None:
        best_class = 0

    return best_class

# computes the accuracy of the individual on a given dataset
def accuracy_ind(ind, data):
    data_x, data_y = data
    if len(data_y) == 0:
        return 0

    y_pred = []
    for attrs in data_x:
        y_pred.append(classify_instance(ind, attrs))

    return accuracy(y_pred, data_y)

def accuracy(pred, gold):
    pred, gold = np.array(pred).round().astype(np.int64), np.array(gold).round().astype(np.int64)
    return sum(pred == gold) / len(pred)


# computes the fitness (accuracy on training data) and objective (error rate
# on testing data)
def fitness(ind, train_data, test_data):
    return utils.FitObjPair(fitness=accuracy_ind(ind, train_data), 
                            objective=1-accuracy_ind(ind, test_data))


# the tournament selection
def tournament_selection(pop, fits, k):
    selected = []
    for _ in range(k):
        p1 = random.randrange(0, len(pop))
        p2 = random.randrange(0, len(pop))
        if fits[p1] > fits[p2]:
            selected.append(copy.deepcopy(pop[p1]))
        else:
            selected.append(copy.deepcopy(pop[p2]))

    return selected

# implements a uniform crossover for individuals with different lenghts
def cross(p1, p2):
    o1, o2 = [], []
    for r1, r2 in zip(p1, p2):
        if random.random() < 0.5:
            o1.append(copy.deepcopy(r1))
            o2.append(copy.deepcopy(r2))
        else:
            o1.append(copy.deepcopy(r2))
            o2.append(copy.deepcopy(r1))
   
    # individuals can have different lenghts
    l = min(len(p1), len(p2))
    rest = o1[l:] + o2[l:]
    for r in rest:
        if random.random() < 0.5:
            o1.append(copy.deepcopy(r))
        else:
            o2.append(copy.deepcopy(r))

    return o1, o2

# class mutation - changes the predicted class for a given rule
def cls_mutate(p, num_classes, mut_cls_prob_change):
    p = copy.deepcopy(p)
    o = []
    for r in p:
        o_cls = r.cls
        if random.random() < mut_cls_prob_change:
            o_cls = random.randrange(0, num_classes)   
        o.append(Rule(conditions=r.conditions, cls=o_cls, priority=r.priority))
    return o

# mutation changing the threshold in conditions in an individual
def cond_mutate(p, mut_cond_sigma):
    o = copy.deepcopy(p)
    for r in o:
        for c in r.conditions:
            c.params += mut_cond_sigma*np.random.randn(*c.params.shape)
    return o

def priority_mutate(p, mut_prio_sigma):
    o = []
    p = copy.deepcopy(p)
    for r in p:
        o_priority = r.priority + mut_prio_sigma*np.random.randn()
        o.append(Rule(conditions=r.conditions, cls=r.cls, priority=o_priority))

    return o

# applies a list of genetic operators (functions with 1 argument - population) 
# to the population
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


# reads data in a csv file
def read_data(filename):
    data_x = []
    data_y = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for line in reader:
            attrs = line[:-1]
            target = line[-1]
            data_x.append(list(map(float, attrs)))
            data_y.append(int(target))

    return (np.array(data_x), np.array(data_y))


def shuffle_data(data):
    data_x, data_y = data

    perm = np.arange(len(data_y))
    np.random.shuffle(perm)

    return (data_x[perm], data_y[perm])


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
#   mutate_ind - reference to the class to mutate an individual - can be used to 
#               change the mutation step adaptively
#   map_fn    - function to use to map fitness evaluation over the whole 
#               population (default `map`)
#   log       - a utils.Log structure to log the evolution run
def evolutionary_algorithm(pop, max_gen, fitness, train_data, test_data, operators, mate_sel, *, map_fn=map, log=None, elitism=1, batch_size=100000):
    evals = 0
    for G in range(max_gen):
        # print("shuffling_data")
        train_x, train_y = shuffle_data(train_data)
        test_x, test_y = shuffle_data(test_data)
        # print("done")

        # evaluate fitness only on a random subset of train/test data up to size batch_size
        # print("evaluating batch of size ", batch_size)
        fit = functools.partial(fitness, train_data=(train_x[:batch_size], train_y[:batch_size]), test_data=(test_x[:0], test_y[:0]))
        fits_objs = list(map_fn(fit, pop))
        # print("done")

        evals += len(pop) * min(len(train_y),  batch_size)


        if log and G%10==0:
            # print("full eval on train + test data")
            full_fit = functools.partial(fitness, train_data=train_data, test_data=test_data)
            fits_objs = list(map_fn(full_fit, pop))
            # print("done")
            log.add_gen(fits_objs, evals)


        fits = [f.fitness for f in fits_objs]

        # print("selection")
        mating_pool = mate_sel(pop, fits, len(pop))
        # print("operators")
        offspring = mate(mating_pool, operators)

        if elitism > 0: 
            # print("selecting first ", elitism, " individuals to survive")
            best_ind = map(lambda x: x[0], sorted(list(enumerate(fits)), key=lambda x: x[1])[-elitism:])
            pop = offspring[elitism:] + [pop[index] for index in best_ind]
            # print("done")
        else:
            pop = offspring[:]

    return pop


def naive(train_y, test_y):
    most_frequent = np.argmax(np.bincount(train_y))
    pred = np.ones(len(test_y)) * most_frequent
    return accuracy(pred, test_y)
    

# xgboost out-of-the-box classifier 
def xgboost(train_x, train_y, test_x, test_y):
    from xgboost import XGBClassifier
    model = XGBClassifier(verbosity=1)
    model.fit(train_x, train_y)

    # make predictions for test data
    y_pred = model.predict(test_x)
    y_pred = [round(value) for value in y_pred]
    # evaluate predictions
    return accuracy(y_pred, test_y)


def train_test_split(input_fn, seed=42):
    # make the split consistent
    np.random.seed(seed)

    # read the data
    data = read_data('inputs/' + input_fn)

    num_attrs = len(data[0][0])
    num_classes = max(data[1]) + 1

    # make training and testing split
    perm = np.arange(len(data[1]))
    np.random.shuffle(perm)
    n_train = 2*len(data[1])//3

    train_x, test_x = data[0][perm[:n_train]], data[0][perm[n_train:]]
    train_y, test_y = data[1][perm[:n_train]], data[1][perm[n_train:]]

    # count the lower and upper bounds
    lb = np.min(train_x, axis=0)
    ub = np.max(train_x, axis=0)

    train_data = (train_x, train_y)
    test_data = (test_x, test_y)

    return train_data, test_data, num_attrs, num_classes, lb, ub


def run_experiment(exp_id="default", input_file="iris.csv", repeats=10, pop_size=100, max_gen=50, cx_prob=0.8, max_rules=10, mut_cls_prob=0.2, mut_cls_prob_change=0.1, mut_cond_prob=0.2, mut_cond_sigma=0.3, 
        mut_prio_sigma=0.3, elitism=1, batch_size=10000, cond_dist=[(LessThen, 0.25), (GreaterThen, 0.25), (Any, 0.5)], priority=False, most_frequent_init=False, print_frequency=1, map_fn=None):

    train_data, test_data, num_attrs, num_classes, lb, ub = train_test_split(input_file)

    cr_ind = functools.partial(create_ind, max_rules=max_rules, 
                               num_attrs=num_attrs, num_classes=num_classes,
                               lb=lb, ub=ub, cond_dist=cond_dist, priority=priority, most_frequent_cls=(-1 if most_frequent_init == False else np.argmax(np.bincount(train_data[1]))))
    xover = functools.partial(crossover, cross=cross, cx_prob=cx_prob)
    cls_mut_ind = functools.partial(cls_mutate, num_classes=num_classes, mut_cls_prob_change=mut_cls_prob_change)
    mut_cls = functools.partial(mutation, mutate=cls_mut_ind, mut_prob=mut_cls_prob)
    mut_cond = functools.partial(mutation, mutate=functools.partial(cond_mutate, mut_cond_sigma=mut_cond_sigma), mut_prob=mut_cond_prob)
    mut_priority = functools.partial(mutation, mutate=functools.partial(priority_mutate, mut_prio_sigma=mut_prio_sigma), mut_prob=mut_cond_prob if priority else 0)

    # run the algorithm `REPEATS` times and remember the best solutions from 
    # last generations

    import multiprocessing

    if map_fn is None:
        pool = multiprocessing.Pool(8)
        map_fn = pool.map

    # fitness computed from the whole dataset
    full_fitness = functools.partial(fitness, train_data=train_data, test_data=test_data)

    best_inds = []
    for run in range(repeats):
        # initialize the log structure
        log = utils.Log(OUT_DIR, exp_id, run, write_immediately=True, print_frequency=print_frequency)
        # create population
        pop = create_pop(pop_size, cr_ind)
        # run evolution - notice we use the pool.map as the map_fn
        pop = evolutionary_algorithm(pop, max_gen, fitness, train_data, test_data, [xover, mut_cls, mut_cond, mut_priority], 
                                     tournament_selection, map_fn=map_fn, log=log, elitism=elitism, batch_size=batch_size)
        # remember the best individual from last generation, save it to file
        bi = max(pop, key=full_fitness)
        best_inds.append(bi)
        
        # if we used write_immediately = False, we would need to save the 
        # files now
        # log.write_files()

    # print an overview of the best individuals from each run
    for i, bi in enumerate(best_inds):
        print(f'Run {i}: objective = {full_fitness(bi).objective}')

    # write summary logs for the whole experiment
    utils.summarize_experiment(OUT_DIR, exp_id)



def hue(name, base_color = (255, 200, 150), low=0, high=100, log=True):
    # scales brightness according to numerical value
    min_intensity = 0.1
    max_intensity = 1

    number = float("".join(list(filter(lambda x: x.isnumeric() or x == ".", name))))
    intensity = (number - low) / (high - low) + min_intensity
    if log:
        base = 2
        low_l = math.log(min_intensity, base)
        high_l = math.log(max_intensity, base)
        intensity = math.log(intensity, base)

        # scale intensity linearly between min_intensity and max_intensity
        intensity = (intensity - low_l) / (high_l - low_l) * (max_intensity - min_intensity) + min_intensity

        

    return tuple(map(lambda x: int(np.clip( intensity * x, 0, 255)), base_color))

def hues(name, low, high, colors_map, log=True):
    for n, color in colors_map:
        if n in name:
            return hue(name, base_color=color, low=low, high=high, log=log)


# separates visually train and test accuracy
def train_test_hue(name, low=0, high=100, train_color = (255, 200, 150), test_color= (150, 200, 255), log=True):
    if ".train" in name:
        return hue(name, train_color, low, high, log)
    elif ".test" in name:
        return hue(name, test_color, low, high, log)



def plot_experiments(*exp_names, log=False, transform_map=lambda x: x, ylim=(0, 1), stat_type=["objective"], color=None, fill=True):
    plt.figure(figsize=(12,8))

    if log:
        plt.yscale("log")

    if ylim is not None:
        plt.ylim(ylim)

    for s in stat_type:
        rename_dict = {}
        for name in exp_names:
            appendix = (".train"  if s == "fitness" else ".test")
            rename_dict[name] = name + appendix

        utils.plot_experiments(OUT_DIR, exp_names, transform_map=transform_map, stat_type=s, rename_dict=rename_dict, color=color, fill=fill)
    plt.show()

if __name__ == '__main__':
    pass

