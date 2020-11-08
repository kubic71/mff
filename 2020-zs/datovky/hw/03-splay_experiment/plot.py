import matplotlib.pyplot as plt
import sys



def plot_file(logfile, label, title, logscale=False):
    plt.figure(figsize=(10, 5))
    plt.title(title)
    plt.xlabel("n")
    plt.ylabel("Average number of rotations per splay")
    n = []
    rotations = []

    if logscale:
        plt.xscale('log')

    with open(logfile, "r") as f:
        for line in f.read().strip().split("\n"):
            line = line.split()

            n.append(int(line[0]))
            rotations.append(float(line[1]))

    #  color = (0, epsilon/0.2, 0)

    plt.plot(n, rotations, label=label)

    plt.scatter(n, rotations)

        
    # plt.fill_between(episodes, lower, upper, alpha=0.25)

    if label is not None:
        plt.legend(loc="upper left")
    plt.savefig("plots/" + logfile.replace("out/", "") + ".png")

    # plt.clf()


def plot_file_subset(logfile, label):
    plt.figure(figsize=(15, 10))
    plt.xlabel("n")
    plt.ylabel("Average number of rotations per splay")
    n = []
    rotations = []
    k = None
    with open(logfile, "r") as f:
        for line in f.read().strip().split("\n") + ["0 0 0"]:
            line = line.split()
            new_k = int(line[0])
            if k is not None and new_k != k:
                plt.plot(n, rotations, label=f"{label}, subset_size={k}")
                plt.scatter(n, rotations)
                n = []
                rotations = []

            k = new_k

            n.append(int(line[1]))
            rotations.append(float(line[2]))

    # plt.fill_between(episodes, lower, upper, alpha=0.25)

    plt.legend(loc="upper left")
    plt.savefig("plots/" + logfile.replace("out/", "") + ".png")


if __name__ == "__main__":
    logfile = sys.argv[1]
