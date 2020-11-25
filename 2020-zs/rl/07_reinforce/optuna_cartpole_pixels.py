import optuna
import os

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--timesteps", default=50000, type=int)
parser.add_argument("--n_trials", default=50, type=int)



def optimize(trial):
    batch_size = int(trial.suggest_loguniform("batch_size", 8, 128))
    # batch_size = 32
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-4, 1e-2)
    gamma = 0.99

    epsilon = trial.suggest_uniform("epsilon", 0.3, 1)
    eps_final = trial.suggest_uniform("epsilon_final", 0.05, 0.2)
    eps_final_at = trial.suggest_uniform("epsilon_final_at", 0.2, 1)
    
    # cs = int(trial.suggest_loguniform("controller_size", 16, 128))
    # cd = trial.suggest_int("controller_depth", 1, 4)
    cs = 64 
    cd = 2

    downsample = trial.suggest_categorical("downsample", [1, 0.5])

    dropout = trial.suggest_uniform("dropout", 0, 0.2)

    # timesteps = int(trial.suggest_uniform("timesteps", 100000, 300000))
    timesteps = 150000

    target_update_interval = 5000

    cmd = f"python cart_pole_pixels.py --batch_size={batch_size} --dropout={dropout} --lr={learning_rate} --gamma={gamma} --cnn_features_dim={cd} --n_hidden={cd}  --total_timesteps={args.timesteps} --target_update_interval={target_update_interval} --downsample={downsample}"
    result = os.popen(cmd).read()
    print(result)
    last_line = result.strip().split("\n")[-1]
    print(last_line)
    score = float(last_line.split()[-2])
    print("score:", score)
    return -score




if __name__ == "__main__":
    args = parser.parse_args()
    study = optuna.create_study()
    study.optimize(optimize, n_trials=args.n_trials)