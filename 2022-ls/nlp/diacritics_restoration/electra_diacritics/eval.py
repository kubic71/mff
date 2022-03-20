from turtle import color
from inference import load_model, diacritize
from compare import comapare_files
import pandas as pd
from tqdm import tqdm
import seaborn as sns   
import matplotlib.pyplot as plt


def plot(path: str):
    # df: pd.DataFrame = pd.DataFrame(columns=["epoch", "word_accuracy", "char_accuracy", "dataset-name"])

    df = load_df()


    # make subplots for word_accuracy and char_accuracy
    fig, ax = plt.subplots(1, 2, figsize=(20,10))
    
    sns.lineplot(x="epoch", y="word_accuracy", data=df, ax=ax[0], hue="dataset-name", style="n_iters")
    sns.lineplot(x="epoch", y="char_accuracy", data=df, ax=ax[1], hue="dataset-name", style="n_iters")

    # save figure
    plt.savefig(path)
    plt.close()

def load_df():

    df = pd.read_csv("accuracy.csv")
    return df


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("--checkpoint", type=str, default="larger-100k")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--n-iters", type=int, default=2)

    args = parser.parse_args()

    if args.plot:
        plot("accuracy.csv", "accuracy.png")
        sys.exit(0)


    params = [
       ("data/diacritics-dtest.txt", "data/diacritics-dtest_stripped.txt", "dev_accuracy"),
       ("data/diacritics-etest.txt", "data/diacritics-etest_stripped.txt", "eval_accuracy"),
    ]


    tmp_fn = "_tmp.txt"


    # df: pd.DataFrame = pd.DataFrame(columns=["epoch", "word_accuracy", "char_accuracy", "dataset-name"])
    df = load_df()
    print(df.head())


    for gold_fn, stripped_fn, plot_fn in params:

        # columns: epoch, word_accuracy, char_accuracy

        for i in range(1000):
            # if dataset-name, epoch, n_iters are already in the df, skip
            if ((df["dataset-name"] == plot_fn) & (df["epoch"] == i) & (df["n_iters"] == args.n_iters)).any():
                print(f"Skipping {plot_fn} epoch {i} n_iters {args.n_iters}")
                continue


            print(f"Epoch {i}")

            try:
                model = load_model(args.checkpoint + "_epoch_" + str(i))
            except FileNotFoundError:
                break

            with open(stripped_fn, "r") as f_in, open("_tmp.txt", "w") as f_out:
                diacritize(f_in, f_out, model, args.n_iters)

            comparison = comapare_files(gold_fn, tmp_fn)

            row = {
                    "epoch": i,
                    "word_accuracy": comparison["correct_words"] / comparison["total_words"],
                    "char_accuracy": comparison["correct_chars"] / comparison["total_chars"],
                    "dataset-name": plot_fn,
                    "n_iters": args.n_iters,
                },

            df = pd.concat([df, pd.DataFrame(row)])
            df.reset_index(drop=True, inplace=True)

            # plot(df, "accuracy.png")

            df.to_csv(f"accuracy.csv")
            plot("accuracy.png")
        