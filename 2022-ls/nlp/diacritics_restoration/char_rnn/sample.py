max_length = 20

# Sample from a category and starting letter
def sample(category, start_letter='A'):
    with torch.no_grad():  # no need to track history in sampling
        category_tensor = categoryTensor(category)
        input = inputTensor(start_letter)
        hidden = rnn.initHidden()

        output_name = start_letter

        for i in range(max_length):
            output, hidden = rnn(category_tensor, input[0], hidden)
            topv, topi = output.topk(1)
            topi = topi[0][0]
            if topi == n_letters - 1:
                break
            else:
                letter = all_letters[topi]
                output_name += letter
            input = inputTensor(letter)

        return output_name

# Get multiple samples from one category and multiple starting letters
def samples(category, start_letters='ABC'):
    for start_letter in start_letters:
        print(sample(category, start_letter))



if __name__ == '__main__':
    import argparse
    import torch
    from model import RNN
    from main import categoryTensor, inputTensor, all_letters, n_letters

    parser = argparse.ArgumentParser(description='Sample from a category and starting letter')
    parser.add_argument('--checkpoint', default='saved_models/rnn_model_50000', type=str, help='path to checkpoint')
    args = parser.parse_args()

    rnn = RNN.load(args.checkpoint)
    rnn.eval()



    samples('Russian', 'RUS')
    samples('German', 'GER')
    samples('Spanish', 'SPA')
    samples('Chinese', 'CHI')
