import optuna
import os

import argparse
import functools
from tsp import *

parser = argparse.ArgumentParser()

parser.add_argument("--exp_id", default="optuna", type=str)
parser.add_argument("--print_frequency", default=10, type=int)

args = parser.parse_args()


def progress_callback(obj, n, trial):
    trial.report(obj, n)

    # Handle pruning based on the intermediate value.
    if trial.should_prune():
        print("Puning!")
        raise optuna.TrialPruned()

def objective(trial):
    pop_size = int(trial.suggest_loguniform("pop_size", 50, 4000))
    generations = int(trial.suggest_loguniform("generations", 50, 500))
    mut_max_len = int(trial.suggest_uniform("mut_max_len", 2, 50))
    mut_prob = trial.suggest_uniform("mut_prob", 0.05, 1)
    cross_prob = trial.suggest_uniform("cross_prob", 0.05, 1)


    cross_set = [edge_recomb_cross, cycle_cross, nwox_cross, pmx_cross]
    mutate_set = [slide_mut, two_opt_mut, swap_mutate]

    cross = trial.suggest_categorical("cross", ["hybrid-random", "hybrid-best", "edge-recomb"])
    cross_map = {"hybrid-best":hybridCrossoverBest(cross_set=cross_set), "hybrid-random":hybridCrossoverRandom(cross_set=cross_set, weights=[1,1,1,1]), "edge-recomb":edge_recomb_cross}


    mutation = trial.suggest_categorical("mutation", ["hybrid-random", "hybrid-best", "swap-mutate", "2-opt"])
    mut_map = {"hybrid-random":hybridMutationRandom(mutate_set=mutate_set, weights=[1, 1, 1]), "hybrid-best":hybridMutationBest(mutate_set=mutate_set),
                "swap-mutate":swap_mutate, "2-opt":two_opt_mut}

    pop_init = trial.suggest_categorical("pop_init", ["random", "nn", "mst"])
    init_func = {"random": create_random_perm, "nn":generate_path_nn, "mst":mst_heuristic}


    score = run_experiment(exp_id=f'{args.exp_id}-mut-{mut_prob}-cross-{cross_prob}-pop-{pop_size}-gen-{generations}', data_input='inputs/tsp_std.in', 
                repeats=1, mut_max_len=mut_max_len, mut_prob=mut_prob, cx_prob=cross_prob, max_gen=generations, pop_size=pop_size, 
               create_ind=init_func[pop_init], cross=cross_map[cross], 
               mutate=mut_map[mutation], print_frequency=args.print_frequency, progress_callback=functools.partial(progress_callback, trial=trial))

    return score




if __name__ == "__main__":
    study = optuna.create_study(study_name="tsp_study_fast", storage="sqlite:///example.db", direction="minimize", load_if_exists=True)
    study.optimize(objective) 