from dataset import DataLoader
from models import LinearInterpolationModel
import matplotlib.pyplot as plt
import seaborn as sns

def boost_lambdas_experiment(model, test_data, dataset_name):
    print("---Boosting trigram-lambda experiment---")
    print("---Evaluation is on test dataset ---")

    original_lambdas = tuple(model.lambdas)

    results = {"boost_percents": [], "cross_entropies": []}

    for boost in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]:
        # add boost-percents of the difference between the trigram lambda and 1.0 to it
        model.lambdas[3] = original_lambdas[3] + boost*(1.0 - original_lambdas[3])

        # scale remaining lambdas, such that the sum of all lambdas is 1.0
        remaining_budget = 1.0 - model.lambdas[3]
        current = original_lambdas[0] + original_lambdas[1] + original_lambdas[2]
        scale = remaining_budget / current

        model.lambdas[0] = original_lambdas[0] * scale
        model.lambdas[1] = original_lambdas[1] * scale
        model.lambdas[2] = original_lambdas[2] * scale

        ce = model.cross_entropy(test_data.get_clean_data())

        results["boost_percents"].append(boost)
        results["cross_entropies"].append(ce)

        print(f"Boost: {boost}\tcross-entropy: {ce:.9f}\tlambdas: {model.lambdas}\t")

    print("----------------------------------------\n\n")
    

    # plot the results
    sns.set(style="whitegrid")
    plt.figure(figsize=(10,5))
    plt.plot(results["boost_percents"], results["cross_entropies"])
    plt.xlabel("Boost percentage")
    plt.ylabel("Test cross-entropy")
    plt.savefig(f"results/{dataset_name}_boost_experiment.png")

    # restore the original lambdas for the next experiment
    model.lambdas = list(original_lambdas)

    return results

def decrease_lambdas_experiment(model, test_data, dataset_name):
    print("---Discounting trigram-lambda experiment---")
    print("---Evaluation is (also) on test dataset ---")

    original_lambdas = tuple(model.lambdas)
    results = {"discount_percents": [], "cross_entropies": []}

    for discount in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        # add boost-percents of the difference between the trigram lambda and 1.0 to it
        model.lambdas[3] = original_lambdas[3]*discount 

        # scale remaining lambdas, such that the sum of all lambdas is 1.0
        remaining_budget = 1.0 - model.lambdas[3]
        current = original_lambdas[0] + original_lambdas[1] + original_lambdas[2]
        scale = remaining_budget / current

        model.lambdas[0] = original_lambdas[0] * scale
        model.lambdas[1] = original_lambdas[1] * scale
        model.lambdas[2] = original_lambdas[2] * scale

        ce = model.cross_entropy(test_data.get_clean_data())
        
        results["discount_percents"].append(discount)
        results["cross_entropies"].append(ce)

        print(f"Discount: {discount}\tcross-entropy: {ce:.9f}\tlambdas: {model.lambdas}\t")


    # plot the results
    sns.set(style="whitegrid")
    plt.figure(figsize=(10,5))
    plt.plot(results["discount_percents"], results["cross_entropies"])
    plt.xlabel("Discount percentage")
    plt.ylabel("Test cross-entropy")
    plt.savefig(f"results/{dataset_name}_discount_experiment.png")

    # restore the original lambdas for the next experiment
    model.lambdas = list(original_lambdas)

    return results


def language_smoothing_experiment(dataset_name):
    print(f"---Language smoothing experiment on {dataset_name} dataset---")

    train_data = DataLoader(f"datasets/{dataset_name}_train.txt")
    heldout_data = DataLoader(f"datasets/{dataset_name}_heldout.txt")
    test_data = DataLoader(f"datasets/{dataset_name}_test.txt")

    print("Fitting the training data...")
    model = LinearInterpolationModel(train_data.get_clean_data(), 3)


    print("Fitting the lambdas on the TRAINING data...")
    model.fit_lambdas(train_data.get_clean_data())

    print(f"Test cross-entropy: {model.cross_entropy(test_data.get_clean_data())}\n\n")


    print("Now fitting the lambdas (correctly) on the HELDOUT data...")
    model.fit_lambdas(heldout_data.get_clean_data())

    print(f"Test cross-entropy: {model.cross_entropy(test_data.get_clean_data())}\n\n")

    boost_lambdas_experiment(model, test_data, dataset_name)
    decrease_lambdas_experiment(model, test_data, dataset_name)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['CZ', 'EN'], default='CZ')
    args = parser.parse_args()

    dataset_name = "TEXTCZ1" if args.dataset == 'CZ' else "TEXTEN1"

    res = language_smoothing_experiment(dataset_name)