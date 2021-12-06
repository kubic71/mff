from models import NGramLanguageModel
from dataset import DataLoader
import pandas as pd


def entropy_experiment(data_file, n_repeats=10):
    """
    Calculates the entropy and perplexity of a dataset using the NGramLanguageModel
    """

    # Load the dataset
    data_loader = DataLoader(data_file)

    results = pd.DataFrame(
        columns=['n', 'entropy', 'perplexity', 'messup_type', 'messup_prob'])

    for messup in ("word", "character"):
        print("Messing-up words")
        for noise_rate in (0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0):
            print("Noise rate: {}".format(noise_rate))
            for i in range(n_repeats):
                print("Repeat {}".format(i))
                # Create the model
                if messup == "word":
                    data = data_loader.mess_up_words(noise_rate)
                elif messup == "character":
                    data = data_loader.mess_up_characters(noise_rate)

                model = NGramLanguageModel(data, n=2)

                # store the results in the panda dataframe
                results = results.append(
                    {
                        'n': 2,
                        'entropy': model.get_model_conditional_entropy(),
                        'perplexity': model.get_model_perplexity(),
                        'messup_type': messup,
                        'messup_prob': noise_rate
                    },
                    ignore_index=True)


    # aggregate multiple runs, compute avg, std, and plot the results
    results = results.groupby(['messup_type', 'messup_prob']).agg(
        {'entropy': ['mean', 'min', 'max'], 'perplexity': ['mean', 'min', 'max']})

    results.reset_index(inplace=True)

    # flatten the dataframe after aggregation
    results.columns = ['messup_type', 'messup_prob', 'entropy_mean', 'entropy_min', 'entropy_max',
                       'perplexity_mean', 'perplexity_min', 'perplexity_max']

    exp_name = data_file.split('/')[-1].split('.')[0] + '_entropy'
    results.to_csv(f'results/{exp_name}.csv', index=False)

    # plot the results
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set(style="whitegrid")

    # plot entropy
    fig, ax = plt.subplots(figsize=(10, 5))

    for messup_type in results['messup_type'].unique():
        # plot entropy
        ax.fill_between(
            results[results['messup_type'] == messup_type]['messup_prob'],
            results[results['messup_type'] == messup_type]['entropy_min'],
            results[results['messup_type'] == messup_type]['entropy_max'],
            alpha=0.2,
            label="_nolegend_")

        # plot the mean entropy and perplexity
        ax.plot(
            results[results['messup_type'] == messup_type]['messup_prob'],
            results[results['messup_type'] == messup_type]['entropy_mean'],
            label=messup_type)

        # add legend
        ax.legend()

        # set x-axis label
        ax.set_xlabel('messup probability')

        # set y-axis label
        ax.set_ylabel('entropy')

        # set title
        ax.set_title('Entropy vs. messup probability')

    # save the figure
    fig.savefig(f'results/{exp_name}.png')
    fig.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        help="input file",
                        default="datasets/TEXTEN1_short.txt")

    args = parser.parse_args()

    res = entropy_experiment(args.input)


    # print(f"Loading {args.input}")
    # data = DataLoader(args.input)
    # print(f"loaded {len(data)} words")

    # model = NGramLanguageModel(data, 2)

    # print("Bigram language model:")
    # print(f"conditional entropy: {model.get_model_conditional_entropy()}")
    # print(f"perplexity: {model.get_model_perplexity()}")
