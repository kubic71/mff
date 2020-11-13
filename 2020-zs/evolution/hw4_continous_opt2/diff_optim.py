import random
import numpy as np
import functools

import co_functions as cf
import utils
import matplotlib.pyplot as plt

DIMENSION = 10  # dimension of the problems
REPEATS = 1  # number of runs of algorithm (should be at least 10)
OUT_DIR = 'continuous'  # output directory for logs
EXP_ID = 'default'  # the ID of this experiment (used to create log names)


# creates the individual
def create_ind(ind_len):
    return np.random.uniform(-5, 5, size=(ind_len,))

def create_pop(pop_size, create_individual):
    return [create_individual() for _ in range(pop_size)]

class PublicVars:
    def __init__(self):
        self.current_gen = 1
        self.fit_func = None

pub_vars = PublicVars()


def differential_evolution(pop, max_gen, differential_op, log=None):
    evals = 0
    for G in range(max_gen):
        pub_vars.current_gen = G

        for i in range(len(pop)):
            differential_op(pop)

        evals += len(pop) 
        fits = [pub_vars.fit_func(ind) for ind in pop]

        if log:
            log.add_gen(fits, evals)
    return pop


cr_ind = functools.partial(create_ind, ind_len=DIMENSION)
# we will run the experiment on a number of different functions
fit_generators = [cf.make_f01_sphere,
                  cf.make_f02_ellipsoidal,
                  cf.make_f06_attractive_sector,
                  cf.make_f08_rosenbrock,
                  cf.make_f10_rotated_ellipsoidal]
fit_names = ['f01', 'f02', 'f06', 'f08', 'f10']

def run_experiment(differential_op, max_gen, pop_size, exp_id=EXP_ID, silent=False):

    # use `functool.partial` to create fix some arguments of the functions
    # and create functions with required signatures

    for fit_gen, fit_name in zip(fit_generators, fit_names):
        fit = fit_gen(DIMENSION)

        for run in range(REPEATS):
            pub_vars.fit_func = fit
            # initialize the log structure
            log = utils.Log(OUT_DIR, exp_id + '.' + fit_name, run,
                            write_immediately=True, print_frequency=5, silent=silent)
            # create population
            pop = create_pop(pop_size, cr_ind)
            pop = differential_evolution(pop, max_gen, differential_op, log=log)

        # write summary logs for the whole experiment
        utils.summarize_experiment(OUT_DIR, exp_id + '.' + fit_name)

