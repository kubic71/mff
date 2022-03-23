import time
from numpy import dtype
import torch
import torch.nn.functional as F
from typing import List, Dict
from torch.functional import F
import torch.nn as nn
import pickle

from transformers import ElectraTokenizerFast, ElectraModel
import torch

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel





class Tokenizer:
    def __init__(self):
        self.tokenizer = ElectraTokenizerFast.from_pretrained("Seznam/small-e-czech")
        self.model = ElectraModel.from_pretrained("Seznam/small-e-czech", output_hidden_states=True)


        self.layers = [-3, -2, -1]


    def get_word_embeddings(self, words: List[str]) -> torch.Tensor:
        sentence = " ".join(words)
        # print("Sentence:", sentence)

        encoded = self.tokenizer.encode_plus(sentence, return_tensors="pt")
        # print("encoded: ", encoded)
        encoded_word_ids = encoded.word_ids()
        # print("encoded_word_ids: ", encoded_word_ids)
        # print(type(encoded_word_ids))
        # print(encoded_word_ids)

        # get all token idxs that belong to the word of interest

        # return get_hidden_states(encoded, token_ids_word, model, layers)
        with torch.no_grad():
            output = self.model(**encoded)

        # Filter Nones at the start and beginning

        states = output.hidden_states
        # print("states", states[-1].shape)
        # Stack and sum all requested layers
        output = torch.stack([states[i] for i in self.layers]).sum(0).squeeze(0)
        # print("output after squeeze", output.shape)

        all_words_embeddings = []
        # print("token_ids", encoded_word_ids)
        for idx in range(len(words)):
            token_ids_word = np.where(np.array(encoded_word_ids) == idx)
            # print("token_ids_word: ", token_ids_word)

            # print corresponding tokens
            # print(self.tokenizer.convert_ids_to_tokens()

            word_tokens_output = output[token_ids_word]
            word_emb = word_tokens_output.mean(dim=0)

            # print("Embedding: ", word_emb.shape, max(word_emb))
            all_words_embeddings.append(word_emb)

        return torch.stack(all_words_embeddings)




class CharCNN(nn.Module):

    def __init__(self, in_channels: int, n_conv_filters: int):
        super(CharCNN, self).__init__()

        self.in_channels = in_channels
        self.n_conv_filters = n_conv_filters

        print("Input CharCNN channels: ", in_channels)
        print("Output CharCNN channels: ", n_conv_filters)

        self.conv1 = nn.Conv1d(in_channels=in_channels, out_channels=n_conv_filters, kernel_size=7, padding="same")
        self.conv2 = nn.Conv1d(in_channels=n_conv_filters, out_channels=n_conv_filters, kernel_size=3, padding="same")
        self.conv3 = nn.Conv1d(in_channels=n_conv_filters, out_channels=n_conv_filters, kernel_size=3, padding="same")

        self.skip = nn.Conv1d(in_channels=in_channels, out_channels=n_conv_filters, kernel_size=1, padding="same")

    def forward(self, input):
        # input shape = (batch_size, in_channels, seq_len)


        # output shape = (batch_size, n_conv_filters, seq_len)
        output = self.conv1(input)
        output = F.relu(output)

        output = self.conv2(output)
        output = F.relu(output)

        output = self.conv3(output)

        # skip connection
        # 1x1 convolution
        skip_output = self.skip(input)

        output = output + skip_output
        return F.relu(output)




class DiacriticModel(nn.Module):

    def __init__(self, char_embedding_dim: int, n_conv_filters: int, char_dict: Dict[str, int], we_dim: int = 64, device='cuda'):
        super(DiacriticModel, self).__init__()

        self.char_dict = char_dict
        self.reverse_char_dict = {v: k for k, v in char_dict.items()}

        self.char_dict_size = len(char_dict)
        self.char_embedding_dim = char_embedding_dim
        self.n_conv_filters = n_conv_filters

        self.char_embedding = nn.Embedding(num_embeddings=self.char_dict_size, embedding_dim=char_embedding_dim)
        self.char_cnn = CharCNN(in_channels=char_embedding_dim + we_dim, n_conv_filters=n_conv_filters)

        # output dense layer, applied to each character separately (sharing weights)
        # maps the output of the char_cnn back to the characters list (char_dict_size)
        self.dense = nn.Linear(in_features=n_conv_filters, out_features=self.char_dict_size)
        self.dropout = nn.Dropout(p=0.2)

        self.tokenizer = Tokenizer()

        self.we_dim = we_dim
        self.word_embedding_projection = nn.Linear(in_features=256, out_features=we_dim)
        self.we_dropout = nn.Dropout(p=0.2)

        self.device = device


        self.ce_loss = nn.CrossEntropyLoss()

        self.we_cache = {}

    def save(self, save_name: str):
        state_dict = self.state_dict()
        model_path = "checkpoints/" + save_name + '.model'
        torch.save(state_dict, model_path)

        # save params
        params = {
            "char_embedding_dim": self.char_embedding_dim,
            "n_conv_filters": self.n_conv_filters,
            "char_dict": self.char_dict,
            "we_dim": self.we_dim,
        }

        # save using pickle

        params_path = "checkpoints/" + save_name + '.params'
        print(f"saving model params to {params_path}, model weights to {model_path}")

        with open(params_path, 'wb') as f:
            pickle.dump(params, f)

    @classmethod
    def load(cls, load_name: str, device='cpu'):
        model_path = "checkpoints/" + load_name + '.model'
        state_dict = torch.load(model_path, map_location=torch.device(device))

        # load params
        params = pickle.load(open(f"checkpoints/{load_name}.params", 'rb'))
        params['device'] = device

        model = cls(**params)
        model.load_state_dict(state_dict)

        return model


    def words_to_indeces(self, words: List[str]) -> torch.Tensor:
        # map each character to its index in the char_dict
        words_indeces = [torch.tensor([self.char_dict[char] for char in word], dtype=torch.long) for word in words]

        # shape = (batch_size, longest_word_len+2)
        return torch.stack(words_indeces)

    def pad_words(self, words: List[str]) -> List[str]:
        # pad each word to the longest word in the batch and add padding character to the beginning and end of each word
        longest_word_len = max([len(word) for word in words])
        padded_words = [" " + word + " "*(longest_word_len - len(word)) + " " for word in words]

        # shape = (batch_size, longest_word_len+2)
        return padded_words

    def diacritize(self, words: List[str]):
        with torch.no_grad():
            outputs: torch.Tensor = self.forward(words)
            # shape = (batch_size, longest_word_len+2, char_dict_size)

            # argmax 
            output_ind = outputs.argmax(dim=2).tolist()
            # shape = (batch_size, longest_word_len+2)

            out_words = []

            for i, word in enumerate(words):
                out_words.append("".join([self.reverse_char_dict[output] for output in output_ind[i][1:len(word)+1]]))

        return out_words

    def forward(self, words_batch: List[str]):
        with torch.no_grad():
            sentence = " ".join(words_batch)
            if sentence in self.we_cache:
                word_embeddings = self.we_cache[sentence]
                # print("Cached")
            else:
                t = time.time()
                word_embeddings = self.tokenizer.get_word_embeddings(words_batch)
                self.we_cache[sentence] = word_embeddings
            # words is a batch of words
            # first we need to pad the words to the same length
            # we should also add padding to the beginning of the words

            word_embeddings = word_embeddings.to(self.device)

            padded_words = self.pad_words(words_batch)
            # print(padded_words)

            # convert to tensor
            char_indices_tensor = self.words_to_indeces(padded_words).to(self.device)

        # print("Char_indices_tensor.shape", char_indices_tensor.shape)
        # char_indices_tesor shape = (batch_size, longest_word_len+2)
        # the +2 is for the padding at the beginning and end of the word

        # feed the char indices to the char embedding layer
        char_embeddings = self.char_embedding(char_indices_tensor)
        # print("Char_embedding.shape", char_embeddings.shape)
        # char_embeddings shape = (batch_size, longest_word_len+2, char_embedding_dim)

        assert word_embeddings.requires_grad == False

        we = self.word_embedding_projection(self.we_dropout(word_embeddings))

        copied_we = we.unsqueeze(1).repeat(1, char_embeddings.shape[1], 1)
        cnn_input = torch.cat((char_embeddings, copied_we), dim=2)

        # we need to convert to channels-first
        cnn_input = cnn_input.permute(0, 2, 1)
        # print("Char_embedding.shape (permuted):", char_embeddings.shape)
        # char_embeddings shape = (batch_size, char_embedding_dim, longest_word_len+2)

        # feed the char embeddings to the char cnn
        char_cnn_outputs = self.char_cnn(cnn_input)
        # apply the dense layer to each character separately, sharing weights

        # char_cnn_outputs shape = (batch_size, 2*n_conv_filters, longest_word_len+2)
        # we need to convert to channels-last
        char_cnn_outputs = char_cnn_outputs.permute(0, 2, 1)
        # print("Char_cnn_outputs.shape (permuted):", char_cnn_outputs.shape)
        # char_cnn_outputs shape = (batch_size, longest_word_len+2, 2*n_conv_filters)

        # concat the original char_embeddings with the char_cnn_outputs
        # dense_input shape = (batch_size, longest_word_len+2, 2*n_conv_filters + char_embedding_dim)
        # dense_input = torch.cat((char_embeddings, char_cnn_outputs), dim=2)
        char_cnn_outputs = self.dense(self.dropout(char_cnn_outputs))
        # print("dense_outputs.shape (dense):", char_cnn_outputs.shape)
        # char_cnn_outputs shape = (batch_size, longest_word_len+2, char_dict_size)

        return char_cnn_outputs

    def loss(self, input_words: List[str], gold_words: List[str]):
        # get the logits
        logits = self(input_words)

        # get the gold labels
        gold_labels = self.words_to_indeces(self.pad_words(gold_words)).to(self.device)

        # logits shape = (batch_size, longest_word_len+2, char_dict_size)
        # gold_labels shape = (batch_size, longest_word_len+2)

        # calculate the cross entropy loss
        loss = self.ce_loss(logits.view(-1, self.char_dict_size), gold_labels.view(-1))

        return loss



if __name__ == "__main__":
    tokenizer = Tokenizer()

    import time
    t = time.time()
    output, encoded, encoded_word_ids = tokenizer.get_word_embeddings("Hlavni mesto Francie je Pariz.".split())
    print("Time: ", time.time() - t)
    # print(word_embedding)