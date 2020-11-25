import matplotlib.pyplot as plt
import sys


from collections import namedtuple

LogData = namedtuple("LogData", ["logfile", "label"])



def plot_file(title:str, save_as:str,logscale:bool, *logDatas:LogData):
    plt.figure(figsize=(10, 5))
    plt.title(title)


    if "Real" in title:
        plt.xlabel("Matrix size")
        plt.ylabel("nanoseconds/item")
    else:
        plt.xlabel("Matrix size")
        plt.ylabel("cache misses/item")

    if logscale:
        plt.xscale('log')

    for data in logDatas:

        n = []
        cache_misses = []
        with open(data.logfile, "r") as f:
            for line in f.read().strip().split("\n"):
                line = line.split()

                n.append(int(line[0]))
                cache_misses.append(float(line[1]))

        #  color = (0, epsilon/0.2, 0)

        plt.plot(n, cache_misses, label=data.label)
        plt.scatter(n, cache_misses)

        
    plt.legend(loc="upper left")
    plt.savefig("plots/" + save_as)




if __name__ == "__main__":
    plot_file("1024 items, 16-item blocks", "m1024b16.png", True, LogData("out/t-sim-m1024-b16-smart", "smart"), LogData("out/t-sim-m1024-b16-naive", "naive"))
    plot_file("8192 items, 64-item blocks", "m8192b64.png", True, LogData("out/t-sim-m8192-b64-smart", "smart"), LogData("out/t-sim-m8192-b64-naive", "naive"))
    plot_file("65536 items, 256-item blocks", "m65536b256.png", True, LogData("out/t-sim-m65536-b256-smart", "smart"), LogData("out/t-sim-m65536-b256-naive", "naive"))
    plot_file("65536 items, 4096-item blocks", "m65536b4096.png", True, LogData("out/t-sim-m65536-b4096-smart", "smart"), LogData("out/t-sim-m65536-b4096-naive", "naive"))

    plot_file("Real hardware - naive from 512", "real_naive_from_512.png", True, LogData("out/t-real-smart", "smart"), LogData("out/t-real-naive", "naive"))


