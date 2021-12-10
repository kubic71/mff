import math
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().splitlines()
    return data

def get_pair_counts_with_distance(data, distance=1):
    pairs = defaultdict(lambda: 0)

    for i in range(len(data) - distance):
        pairs[data[i], data[i + distance]] += 1
    
    return pairs

def get_word_counts(data):
    word_counts = defaultdict(lambda: 0)
    for word in data:
        word_counts[word] += 1
    return word_counts

def get_pmi(pair_counts, word_counts):
    """Compute pointwise mutual information of word pairs."""

    n = sum(word_counts.values())
    mut_information = defaultdict(lambda: float("-inf"))

    for (x, y), count in pair_counts.items():
        # Compute pmi

        pmi = math.log2(count * n / (word_counts[x] * word_counts[y]))
        # Store in dictionary
        mut_information[(x, y)] = pmi

    return mut_information

def best_distanced_friends(data, dataset_name, max_distance=50):
    """Find the best friends with a distance not greater than max_distance.
    """
    
    best_friends = []

    for i in range(1, max_distance + 1):
        pair_counts = get_pair_counts_with_distance(data, distance=i)
        word_counts = get_word_counts(data)

        mut_information = get_pmi(pair_counts, word_counts)

        # Filter out pairs, in which one of the words appears less than 10 times
        filtered_mut_information = {k: v for k, v in mut_information.items() if word_counts[k[0]] > 10 and word_counts[k[1]] > 10}

        # Get top 20 pairs
        top_pairs = sorted(filtered_mut_information.items(), key=lambda x: x[1], reverse=True)[:20]

        # add these to best_friends, along with the distance
        for pair, pmi in top_pairs:
            best_friends.append((i, pair, pmi))


    top_pairs = sorted(best_friends, key=lambda x: x[2], reverse=True)[:20]
    # Show the best 20 pairs
    for distance, pair, pmi in top_pairs:
        print(f"{distance} {pair[0]} {pair[1]} {pmi}")

    plt.figure(figsize=(12, 8))
    sns.barplot(y=[f"({str(distance)}) {' '.join(pair)}" for distance, pair, pmi in top_pairs], x=[pmi for distance, pair, pmi in top_pairs])
    
    plt.title(f"Best friends with distance not greater than {max_distance}")
    plt.xlabel("Pointwise Mutual Information")
    plt.ylabel("Word pair, distance")
    plt.tight_layout()
    plt.savefig(f"results/best_distanced_friends_{dataset_name}.png")

def best_bigram_friends(data, dataset_name):
    """Find the best bigram friends.
    """
    pair_counts = get_pair_counts_with_distance(data, distance=1)
    word_counts = get_word_counts(data)

    mut_information = get_pmi(pair_counts, word_counts)

    # Filter out pairs, in which one of the words appears less than 10 times
    filtered_mut_information = {k: v for k, v in mut_information.items() if word_counts[k[0]] > 10 and word_counts[k[1]] > 10}

    # Get top 20 pairs
    top_pairs = sorted(filtered_mut_information.items(), key=lambda x: x[1], reverse=True)[:20]


    # Show the best 20 pairs 
    for pair, pmi in top_pairs:
        print("{} {} {}".format(pair[0], pair[1], pmi))


    # plot barplot of the top pairs, with PMI as bar height and the pair as caption
    # make the captions vertical
    plt.figure(figsize=(12, 8))
    sns.barplot(y=[" ".join(pair) for pair, pmi in top_pairs], x=[pmi for pair, pmi in top_pairs])
    plt.title(f"Best bigram friends")
    plt.xlabel("Pointwise Mutual Information")
    plt.ylabel("Word pair")
    plt.tight_layout()
    plt.savefig(f"results/best_bigram_friends_{dataset_name}.png")



if __name__ == "__main__":
    
    print("---Best Czech friends---")
    data = load_data('datasets/TEXTCZ1.txt')
    best_bigram_friends(data, "czech")

    print("\n\n---Best English friends---")
    data = load_data('datasets/TEXTEN1.txt')
    best_bigram_friends(data, "english")


    print("\n\n---Best Czech friends with distance up to 50---")   
    data = load_data('datasets/TEXTCZ1.txt')
    best_distanced_friends(data, "czech", max_distance=50)

    print("\n\n---Best English friends with distance up to 50---")   
    data = load_data('datasets/TEXTEN1.txt')
    best_distanced_friends(data, "english", max_distance=50)