from dataset import DataLoader


def get_frequencies(data):
    freq_dict = {}
    for word in data:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict


def plot_the_most_common_words(freq_dict, dataset_name, k=50):

    most_common_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:k]
    most_common = [(word, freq_dict[word]) for word in most_common_words]


    # plot most common words as a bar chart
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set(style="darkgrid")

    fig, ax = plt.subplots(figsize=(15, 10))

    # set the title
    ax.set_title(f"Most {len(most_common)} common words in {dataset_name}")

    # plot the bar chart
    # make the words labels of the y-axis, such that the most common words are at the top
    ax.barh(range(len(most_common)), [x[1] for x in most_common], align="center")

    # set the labels of the y-axis
    ax.set_yticks(range(len(most_common)))
    ax.set_yticklabels([x[0] for x in most_common])

    # map the color of the bars to the frequency of the words
    ax.set_xlabel("Frequency")
    rainbow = plt.get_cmap("rainbow")

    colors = []
    max_freq = max([x[1] for x in most_common])

    for i in range(len(most_common)):
        freq = most_common[i][1]
        c = freq / max_freq

        # make the transition between the colors more smooth
        c = c ** 0.2

        colors.append(rainbow(c))


    for i, rect in enumerate(ax.patches):
        rect.set_facecolor(colors[i])


    # save the figure
    fig.savefig('results/most_common_words_{}.png'.format(dataset_name))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Basic language statistics")
    parser.add_argument("-i",
                        "--input",
                        help="input file",
                        default="datasets/TEXTEN1.txt")

    args = parser.parse_args()
    
    dataset_name = args.input.split("/")[-1].split(".")[0]

    dl = DataLoader(path=args.input)

    words = dl.get_clean_data()

    print("Dataset: {}".format(dataset_name))

    # compute basic language dataset statistics
    print(f"Number of words: {len(words)}")

    # compute the vocabulary
    print(f"Number of unique words: {len(dl.vocab)}")

    freq_dict = get_frequencies(words)

    # number of words occurring only once
    num_once = sum([1 for x in freq_dict.values() if x == 1])
    print(f"Number of words occurring only once: {num_once}")


    plot_the_most_common_words(freq_dict, dataset_name)
