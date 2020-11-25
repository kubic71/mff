import matplotlib.pyplot as plt
import os 
import sys
import argparse


# parser.add_argument("--epsilon", default = None, type=float)
# parser.add_argument("--gamma", default = None, type=float)
# parser.add_argument("--epsilon", default = None, type=float)


if len(sys.argv) == 1:
    logs = os.listdir("logs/")
else:
    logs = sys.argv[1:]


print(logs)
for log in logs:
    # epsilon = list(map(lambda param: float(param.split("=")[1]), log.split(",")))

    # if args.boxes is not None and args.boxes != boxes:
    #     continue

    # if args.epsilon is not None and args.epsilon != epsilon:
    #     continue

    with open("logs/"+ log, "r") as logfile:
        episodes = []
        means = []

        # lower = []
        # upper = []

        for line in logfile.read().strip().split("\n"):
            line = line.split()
            
            if len(line) < 2:
                # partial log file
                break

            try:
                episodes.append(int(line[0]))
                means.append(float(line[1]))

            except ValueError:
                print("Bad number format")

            # std = float(line[2])
            # lower.append(means[-1] - std)
            # upper.append(means[-1] + std)

        #  color = (0, epsilon/0.2, 0)

        plt.plot(episodes, means, label=log)

        # plt.fill_between(episodes, lower, upper, alpha=0.25)

plt.legend()
plt.show()
