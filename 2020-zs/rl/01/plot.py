import matplotlib.pyplot as plt
import os 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--boxes", default= None, type=int)
parser.add_argument("--epsilon", default = None, type=float)

args = parser.parse_args()

logs = os.listdir("logs/")


for log in logs:
    boxes, epsilon = list(map(lambda param: float(param.split("=")[1]), log.split(",")))

    if args.boxes is not None and args.boxes != boxes:
        continue

    if args.epsilon is not None and args.epsilon != epsilon:
        continue

    with open("logs/"+ log, "r") as logfile:
        episodes = []
        means = []
        lower = []
        upper = []

        for line in logfile.read().strip().split("\n"):
            line = line.split()
            episodes.append(int(line[0]))
            means.append(float(line[1]))
            std = float(line[2])
            lower.append(means[-1] - std)
            upper.append(means[-1] + std)

        #  color = (0, epsilon/0.2, 0)

        plt.plot(episodes, means, label=log )
        # plt.fill_between(episodes, lower, upper, alpha=0.25)

plt.legend()
plt.show()
