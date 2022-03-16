from model import DiacriticModel
from matplotlib import pyplot as plt
import torch
from tqdm import tqdm
import random
from collections import defaultdict

# from diacritization_stripping import strip_diacritization_uninorms

# a á b c č d ď e é ě f g h ch i í j k l m n ň o ó p q r ř s š t ť u ů ú v w x y ý z ž
# á č ď é ě í ň ó ř š ť ú ů ý ž

strip_map = {
"á": "a", 
"č": "c",
"ď": "d",
"é": "e",
"ě": "e",
"í": "i",
"ň": "n",
"ó": "o",
"ř": "r",
"š": "s",
"ť": "t",
"ú": "u",
"ů": "u",
"ý": "y",
"ž": "z"
}


# everything is lowercase, no collision problem
UNKNOWN_SYMBOL = "U"

def load_sentences(path="data/sentences.txt", max_sentences=1000, min_freq_char=20):
    char_freq = defaultdict(lambda: 0)


    with open(path, 'r') as f:
        lines = []
        for i in tqdm(range(max_sentences)):
            line = f.readline().strip()

            # add all characters to set
            for c in line:
                char_freq[c] += 1

            lines.append(line.split())

    # filter out chars with low frequency 
    chars = set([c for c, freq in char_freq.items() if freq > min_freq_char])

    for c, f in sorted(char_freq.items(), key=lambda x: x[1], reverse=True):
        if c in chars:
            print(c, f)
    
    assert UNKNOWN_SYMBOL not in chars
    chars.add(UNKNOWN_SYMBOL)
    
    filtered_lines = []
    for line in lines:
        new_line = []   
        for word in line:
            new_word = []
            for c in word:
                if c in chars:
                    new_word.append(c)
                else:
                    new_word.append(UNKNOWN_SYMBOL)
            new_line.append("".join(new_word))
        
        filtered_lines.append(new_line)

    return chars, filtered_lines

def strip_diacritics(sentences, prob=0.5):
    strip_chars = set()

    num_diacritics = 0
    total_chars = 0


    stripped = []
    for sentence in sentences:
        stripped_sentence = []

        for word in sentence:
            stripped_word = []
            for char in word:
                total_chars += 1
                if char in strip_map:
                    num_diacritics += 1
                    if random.random() < prob:
                        c = strip_map[char]
                    else:
                        c = char
                else:
                    c = char
                stripped_word.append(c)
                strip_chars.add(c)
            
            stripped_sentence.append("".join(stripped_word))
        
        s1 =" ".join(sentence)
        s2 = " ".join(stripped_sentence)

        assert len(sentence) != 0

        assert len(s1) == len(s2)
        # print(len(s1), len(s2))
        stripped.append(stripped_sentence)

        # print(" ".join(stripped_sentence))

    print(f"num diacritics = {num_diacritics}/{total_chars} = {num_diacritics/total_chars}")
    return strip_chars, stripped


def batches(dataset, batch_size=100):
    sentences, gold_sentences = dataset
    x_batch = []
    y_batch = []
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            x_batch.append(sentences[i][j])
            y_batch.append(gold_sentences[i][j])

            if len(x_batch) == batch_size:
                yield x_batch, y_batch
                x_batch = []
                y_batch = []

    if len(x_batch) > 0:
        yield x_batch, y_batch



def plot(all_losses, path="diacritizator_losses.png"):
    plt.plot(all_losses)
    plt.savefig(path)
    plt.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Train a character-level diacritization model')

    parser.add_argument('--exp-name', type=str, default='diacritic_model')
    parser.add_argument('--max-sentences', type=int, default=2000)
    parser.add_argument('--train-test-split', type=float, default=0.95)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--strip-prob', type=float, default=0.5)


    args = parser.parse_args()
    chars, sentences = load_sentences(max_sentences=args.max_sentences)


    strip_chars, stripped = strip_diacritics(sentences, prob=args.strip_prob)

    # check that all strip chars are in chars
    assert strip_chars.issubset(chars)

    char_dict = {}
    for i, c in enumerate(sorted(list(chars))):
        print(f"{i} {c}")
        char_dict[c] = i


    train_n = int(len(stripped) * args.train_test_split)
    test_n = len(stripped) - train_n

    train = stripped[:train_n], sentences[:train_n]
    test = stripped[train_n:], sentences[train_n:]


    model: torch.nn.Module = DiacriticModel(char_embedding_dim=32, n_conv_filters=64, char_dict=char_dict)

    learning_rate = 0.005
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    all_losses = []

    for epoch in range(args.epochs):
        total_loss = 0

        for x_batch, y_batch in tqdm(batches(train, batch_size=100)):

            optimizer.zero_grad()
            model.zero_grad()

            loss = model.loss(x_batch, y_batch)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        
        all_losses.append(total_loss)
        plot(all_losses)

        print(f"epoch {epoch} loss = {total_loss}")

    
        # evaluate on test set
        for x_batch, y_batch in tqdm(batches(test, batch_size=100)):
            pred = model.diacritize(x_batch)
            
            print("Strip:\t", " ".join(x_batch))
            print("Gold:\t", " ".join(y_batch))
            print("Pred:\t", " ".join(pred))
            print()
