import optuna
import os

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--episodes", default=200, type=int)
parser.add_argument("--n_trials", default=100, type=int)



def optimize(trial):
    # batch_size = int(trial.suggest_loguniform("batch_size", 16, 4096))
    batch_size = 16
    # learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-2)
    learning_rate = 0.01
    # gamma = trial.suggest_categorical("gamma", [0.9, 0.99, 0.999])
    gamma = 0.999
    
    hidden_layer_size  = int(trial.suggest_loguniform("hidden_layer_size", 4, 32))
    hidden_layers = int(trial.suggest_int("hidden_layers", 2, 4))

    # activation = trial.suggest_categorical("activation", ["tanh", "relu"])
    activation = "tanh"

    dropout = trial.suggest_uniform("dropout", 0, 0.5)


    cmd = f"python reinforce.py --batch_size={batch_size} --dropout={dropout} --learning_rate={learning_rate} --gamma={gamma} --hidden_layer_size={hidden_layer_size} --hidden_layers={hidden_layers} --activation={activation} --episodes={args.episodes}"
    last_line = os.popen(cmd).read().strip().split("\n")[-1]
    print(last_line)
    score = float(last_line.split()[-2])
    print("score:", score)
    return -score




if __name__ == "__main__":
    args = parser.parse_args()
    study = optuna.create_study()
    study.optimize(optimize, n_trials=args.n_trials)