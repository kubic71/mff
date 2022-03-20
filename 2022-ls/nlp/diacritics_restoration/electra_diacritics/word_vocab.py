from strip import strip_string
from typing import Dict
from nltk import word_tokenize
import pickle

def save_vocab(vocab, strip_vocab):
    with open("vocab.pkl", "wb") as f:
        pickle.dump(vocab, f)
    with open("strip_vocab.pkl", "wb") as f:
        pickle.dump(strip_vocab, f)

def load_vocab(min_freq=1):
    with open("vocab.pkl", "rb") as f:
        vocab = pickle.load(f)
    with open("strip_vocab.pkl", "rb") as f:
        strip_vocab: Dict[str, Dict[str, int]] = pickle.load(f)

    for strip_w in strip_vocab:
        strip_vocab[strip_w] = {w: i for w, i in strip_vocab[strip_w].items() if i >= min_freq}
        

    return vocab, strip_vocab



    

    return vocab, strip_vocab


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/sentences_full.txt") 

    args = parser.parse_args()

    strip_vocab = {}
    vocab = set()

    with open(args.input, "r") as f:
        i = 0
        for line in f:
            i += 1

            if i % 10000 == 0:
                print(i)

            for token in word_tokenize(line):
                token = token.lower()

                vocab.add(token)

                stripped = strip_string(token)
                if stripped not in strip_vocab:
                    strip_vocab[stripped] = {token: 1}

                else:
                    if token not in strip_vocab[stripped]:
                        strip_vocab[stripped][token] = 1
                    else:
                        strip_vocab[stripped][token] += 1
                

    save_vocab(vocab, strip_vocab)

    print(len(vocab))