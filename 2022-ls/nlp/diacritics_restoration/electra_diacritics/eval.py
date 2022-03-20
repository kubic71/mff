from inference import load_model, diacritize
from compare import comapare_files
import pandas as pd
from tqdm import tqdm
import seaborn as sns   
import matplotlib.pyplot as plt


def plot(df: pd.DataFrame, path: str):
    # df: pd.DataFrame = pd.DataFrame(columns=["epoch", "word_accuracy", "char_accuracy", "dataset-name"])

    # make subplots for word_accuracy and char_accuracy
    fig, ax = plt.subplots(1, 2, figsize=(20,10))
    sns.lineplot(x="epoch", y="word_accuracy", data=df, ax=ax[0], hue="dataset-name")
    sns.lineplot(x="epoch", y="char_accuracy", data=df, ax=ax[1], hue="dataset-name")

    # save figure
    plt.savefig(path)
    plt.close()



if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("--checkpoint", type=str, default="larger-100k")
    parser.add_argument("--plot", action="store_true")

    args = parser.parse_args()

    if args.plot:
        df = pd.read_csv("accuracy.csv")
        plot(df, "accuracy.png")
        sys.exit(0)


    params = [
       ("data/diacritics-dtest.txt", "data/diacritics-dtest_stripped.txt", "dev_accuracy.png"),
       ("data/diacritics-etest.txt", "data/diacritics-etest_stripped.txt", "eval_accuracy.png"),
    ]


    tmp_fn = "_tmp.txt"

    df: pd.DataFrame = pd.DataFrame(columns=["epoch", "word_accuracy", "char_accuracy", "dataset-name"])
    for gold_fn, stripped_fn, plot_fn in params:

        # columns: epoch, word_accuracy, char_accuracy

        for i in range(1000):
            print(f"Epoch {i}")

            try:
                model = load_model(args.checkpoint + "_epoch_" + str(i))
            except FileNotFoundError:
                break

            with open(stripped_fn, "r") as f_in, open("_tmp.txt", "w") as f_out:
                diacritize(f_in, f_out, model)

            comparison = comapare_files(gold_fn, tmp_fn)

            row = {
                    "epoch": i,
                    "word_accuracy": comparison["correct_words"] / comparison["total_words"],
                    "char_accuracy": comparison["correct_chars"] / comparison["total_chars"],
                    "dataset-name": plot_fn,
                },

            df = pd.concat([df, pd.DataFrame(row)])

            # plot(df, "accuracy.png")

    df.to_csv("accuracy.csv")

