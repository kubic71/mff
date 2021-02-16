import argparse
from tsp import *

parser = argparse.ArgumentParser()


parser.add_argument("--mut-max-len", default=10, type=int)
parser.add_argument("--print-frequency", default=10, type=int)

parser.add_argument("--mut-prob", default=0.5, type=float)
parser.add_argument("--cross-prob", default=0.8, type=float)
parser.add_argument("--pop-size", default=2000, type=int)
parser.add_argument("--gen", default=5000, type=int)

cross_set = [edge_recomb_cross, cycle_cross, nwox_cross, pmx_cross]
mutate_set = [slide_mut, two_opt_mut, swap_mutate]

parser.add_argument("--cross", default="hybrid-best", type=str, choices=["hybrid-best", "hybrid-random", "cycle"])
cross_map = {"hybrid-best":hybridCrossoverBest(cross_set=cross_set), "hybrid-random":hybridCrossoverRandom(cross_set=cross_set, weights=[1,1,1,1]), "cycle":cycle_cross}

parser.add_argument("--pop-init", default="random", type=str, choices=["random", "nn", "mst", "hybrid"])
init_func = {"random": create_random_perm, "nn":generate_path_nn, "mst":mst_heuristic, "hybrid":hybrid_ind([create_random_perm, generate_path_nn, mst_heuristic], [1,1,1])}

parser.add_argument("--exp-id", default="hybrid-cross-best-mut-random")


mutation = parser.add_argument("--mutation", default="hybrid-random", choices=["hybrid-random", "hybrid-best", "swap-mutate", "2-opt", "slide-mutate"])
mut_map = {"hybrid-random":hybridMutationRandom(mutate_set=mutate_set, weights=[1, 1, 1]), "hybrid-best":hybridMutationBest(mutate_set=mutate_set),
                "swap-mutate":swap_mutate, "2-opt":two_opt_mut, "slide-mutate":slide_mut}


args = parser.parse_args()


run_experiment(exp_id=f'{args.exp_id}-mut-{args.mut_prob}-cross-{args.cross_prob}-pop-{args.pop_size}-gen-{args.gen}', data_input='inputs/tsp_std.in', 
                repeats=1, mut_max_len=args.mut_max_len, mut_prob=args.mut_prob, cx_prob=args.cross_prob, max_gen=args.gen, pop_size=args.pop_size, 
               create_ind=init_func[args.pop_init], cross=cross_map[args.cross], 
               mutate=mut_map[args.mutation],
               print_frequency=args.print_frequency)
