from model import DiacriticModel
from matplotlib import pyplot as plt
from strip import strip_string
from train import strip_map, UNKNOWN_SYMBOL
from typing import Dict, List, Text, Tuple, TextIO, Set

from nltk.tokenize import word_tokenize

from word_vocab import load_vocab

import torch

def word_tokenize2(tokens):
    return [token.replace("''", '"').replace("``", '"') for token in word_tokenize(tokens)]


def tokenize(sentence: str) -> List[Tuple[int, str]]:
    # use NLTK to tokenize the sentence into string tokens and their positions in the sentence
    tokens = []
    offset = 0
    for token in word_tokenize2(sentence):
        offset = sentence.find(token, offset)
        tokens.append((offset, token))
        offset += len(token)

    return tokens



def token_map(tokens: List[Tuple[int, str]], map_fn):
    result = []
    for ind, token in tokens:
        result.append((ind, "".join(list(map(map_fn, token)))))
    
    return result

def token_filter(tokens: List[Tuple[int, str]], filter_fn):
    filtered = []
    for ind, token in tokens:
        if filter_fn(token):
            filtered.append((ind, token))
    
    return filtered

def token_join(tokens: List[Tuple[int, str]], fill_with=" "):
    result = []
    for ind, token in tokens:
        for _ in range(ind - len(result)):
            result.append(fill_with)
        
        result.extend(list(token))

    return "".join(result)

def token_strip_map(char: str, char_dict: Dict[str, str]):
    char = char.lower()

    if char in strip_map:
        return strip_map[char]
    elif char in char_dict:
        return char
    else:
        return UNKNOWN_SYMBOL

def load_test_data(file_input, char_dict: Dict[str, str]):
    orig = []
    stripped = []

    for line in file_input:
        line = line.strip()
        words = tokenize(line)
        orig.append(words)
        strip = token_map(words, lambda char: token_strip_map(char, char_dict))
        stripped.append(token_filter(strip, lambda token: token != " "))

    return orig, stripped

def merge_token(orig: str, pred: str):
    assert len(orig) == len(pred)

    res = []
    for o, p in zip(orig, pred):
        if o != p:
            if p in strip_map:
                if o.isupper():
                    res.append(p.upper())
                else:
                    res.append(p)
            else:
                res.append(o)
        else:
            res.append(o)
    
    return "".join(res)


def diacritization_merge(orig: List[Tuple[int, str]], stripped: List[Tuple[int, str]], pred: List[str]) -> str:
    assert len(stripped) == len(pred)

    if len(orig) == 0:
        return ""
    elif len(stripped) == 0:
        return token_join(orig)

    current_stripped_index = 0
    next_position = stripped[current_stripped_index][0]

    result = []


    for ind, token in orig:
        if next_position > ind:
            result.append((ind, token))

        else:
            assert stripped[current_stripped_index][0] == ind
            assert len(stripped[current_stripped_index][1]) == len(token)

            result.append((ind, merge_token(token, pred[current_stripped_index])))
            current_stripped_index += 1

            # check if we are at the end of the stripped list
            if current_stripped_index < len(stripped):
                next_position = stripped[current_stripped_index][0]
            else:
                # infinity
                next_position = float("inf")

    return token_join(result)

def dictionary_autocorrect(tokens: List[str], strip_vocab: Dict[str, Dict[str, int]]):

    new_tokens = []

    for orig_token in tokens:
        token = strip_string(orig_token)

        if token in strip_vocab and len(strip_vocab[token]) == 1:
            k, v = list(strip_vocab[token].keys())[0], list(strip_vocab[token].values())[0]
            new_tokens.append(k)

        else:
            new_tokens.append(orig_token)
    return new_tokens

def dictionary_autocorrect2(pred_tokens: List[str], vocab: Set[str], strip_dict: Dict[str, str]):
    new_tokens = []

    for token in pred_tokens:
        stripped_token = strip_string(token)

        if token not in vocab and stripped_token in strip_dict:
            # take the token with the highest frequency
            best_guess = sorted(strip_dict[stripped_token].items(), key=lambda x: x[1], reverse=True)[0][0]
            new_tokens.append(best_guess)
        
        else:
            new_tokens.append(token)
    
    return new_tokens



def diacritize(input: TextIO, output: TextIO, model: DiacriticModel, n_iters: int = 1, use_dict=True):
    if use_dict:
        vocab, strip_vocab = load_vocab()

    orig, stripped = load_test_data(input, model.char_dict)
    assert len(orig) == len(stripped)

    for i, orig_sentence in enumerate(orig):
        stripped_sentence = stripped[i]
        stripped_tokens = [token for _, token in stripped_sentence]


        if len(stripped_sentence) == 0:
            pred_sentence = []
        else:
            pred_sentence = stripped_tokens

            for _ in range(n_iters):
                pred_sentence = model.diacritize(pred_sentence)

            if use_dict:
                print("Autocorrect:")
                print(" ".join(pred_sentence))
                pred_sentence = dictionary_autocorrect(pred_sentence, strip_vocab)
                print(" ".join(pred_sentence))

                pred_sentence = dictionary_autocorrect2(pred_sentence, vocab, strip_vocab)
            

        # detokenize
        pred_merged = diacritization_merge(orig_sentence, stripped_sentence, pred_sentence)
        output.write(pred_merged + "\n")

        orig_str = token_join(orig_sentence)

        assert len(orig_str) == len(pred_merged)


def load_model(checkpoint_name: str):
    model = DiacriticModel.load(checkpoint_name)
    model.device = 'cpu'
    model = model.cpu()
    model.eval()

    return model


if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument("--checkpoint", type=str, default="final-100000k_epoch_65")
    parser.add_argument("--n-iters", type=int, default=1)
    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--use-dict", action="store_true")

    args = parser.parse_args()

    if args.input is None:
        # default is stdin
        input_stream = sys.stdin
    else:
        input_stream = open(args.input, "r")

    if args.output is None:
        # default is stdout
        output_stream = sys.stdout
    else:
        output_stream = open(args.output, "w")

    
    model = load_model(args.checkpoint)
    diacritize(input_stream, output_stream, model, args.n_iters, args.use_dict)