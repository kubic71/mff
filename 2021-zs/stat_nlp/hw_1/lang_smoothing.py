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
        model.lambdas[3] = original_lambdas[3]*(1-discount)

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


    # restore the original lambdas for the next experiment
    model.lambdas = list(original_lambdas)

    return results


def language_smoothing_experiment():
    import pandas as pd

    # create boost_results pandas dataframe with colums: boost_percent, cross_entropy, dataset_name
    boost_results_df = pd.DataFrame(columns=["boost_percents", "cross_entropies", "dataset_name"])


    # create boost_results pandas dataframe with colums: discount_percent, cross_entropy, dataset_name
    discount_results_df = pd.DataFrame(columns=["discount_percents", "cross_entropies", "dataset_name"])

    for dataset_name in ["TEXTCZ1", "TEXTEN1"]:
        print(f"---Language smoothing experiment on {dataset_name} dataset---")

        train_data = DataLoader(f"datasets/{dataset_name}_train.txt")
        heldout_data = DataLoader(f"datasets/{dataset_name}_heldout.txt")
        test_data = DataLoader(f"datasets/{dataset_name}_test.txt")

        print("Fitting the training data...")
        model = LinearInterpolationModel(train_data.get_clean_data(), 3)


        print("Fitting the lambdas on the TRAINING data...")
        # model.fit_lambdas(train_data.get_clean_data())

        print(f"Test cross-entropy: {model.cross_entropy(test_data.get_clean_data())}\n\n")


        print("Now fitting the lambdas (correctly) on the HELDOUT data...")
        model.fit_lambdas(heldout_data.get_clean_data())

        print(f"Test cross-entropy: {model.cross_entropy(test_data.get_clean_data())}\n\n")


        boost_results = boost_lambdas_experiment(model, test_data, dataset_name)
        boost_results["dataset_name"] = "Czech" if dataset_name=="TEXTCZ1" else "English"
        boost_results_df = boost_results_df.append(pd.DataFrame(boost_results),  ignore_index=True)

        discount_results = decrease_lambdas_experiment(model, test_data, dataset_name)
        discount_results["dataset_name"] = "Czech" if dataset_name=="TEXTCZ1" else "English"
        discount_results_df = discount_results_df.append(pd.DataFrame(discount_results), ignore_index=True)


    # plot with seaborn
    import seaborn as sns

    sns.set(style="darkgrid")

    # plot boost_results
    plt.figure(figsize=(9, 6))
    sns.lineplot(x="boost_percents", y="cross_entropies", data=boost_results_df, hue="dataset_name", marker="o", legend="brief")
    plt.title("Boosting trigram-lambda experiment")
    plt.xlabel("Boost percentage")
    plt.ylabel("Cross-entropy")
    plt.savefig("results/boost_experiment.png")

    # plot discount_results
    plt.figure(figsize=(9, 6))
    sns.lineplot(x="discount_percents", y="cross_entropies", data=discount_results_df, hue="dataset_name", marker="o", legend="brief")
    plt.title("Discounting trigram-lambda experiment")
    plt.xlabel("Discount percentage")
    plt.ylabel("Cross-entropy")
    plt.savefig("results/discount_experiment.png")








if __name__ == '__main__':
    res = language_smoothing_experiment()
