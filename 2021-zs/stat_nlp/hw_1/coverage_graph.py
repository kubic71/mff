from dataset import DataLoader
from models import NGram, ngram_iterator




def compute_coverage(dataset_name):
    """
    Plot the coverage graph, defined as the percentage of words in the test data which have been seen in the training data
    """


    # Load the data
    trainset = DataLoader(path=f"datasets/{dataset_name}_train.txt").get_clean_data()
    testset = DataLoader(path=f"datasets/{dataset_name}_test.txt").get_clean_data()


    coverage = {"n": [], "coverage": []}

    for n in range(1, 5):
        train_ngram = NGram(n, trainset)
        test_ngram = NGram(n, testset)

        # Get the coverage
        coverage["n"].append(n)

        total_ngrams = 0
        covered_ngrams = 0
        for ngram, _ in ngram_iterator(testset, n):
            if train_ngram.get_ngram_count(ngram) > 0:
                covered_ngrams += 1
            total_ngrams += 1

        coverage["coverage"].append(covered_ngrams / total_ngrams)

    return coverage


def plot_coverage():

    cov_cz = compute_coverage("TEXTCZ1")
    cov_en = compute_coverage("TEXTEN1")


    import seaborn as sns
    import matplotlib.pyplot as plt
        
    # plot coverage histogram
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(cov_cz["n"], cov_cz["coverage"], label="Czech", marker="o")
    ax.plot(cov_en["n"], cov_en["coverage"], label="English", marker="o")
    ax.set_xlabel("N-gram size")
    ax.set_ylabel("Coverage")
    ax.set_title("Coverage of the test data")
    ax.legend()
    # save figure
    fig.savefig("results/coverage.png")





if __name__ == '__main__':
    plot_coverage()
