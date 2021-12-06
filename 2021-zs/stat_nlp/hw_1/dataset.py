import random
class DataLoader:
    def __init__(self, path="datasets/TEXTCZ1.txt"):
        self.path = path

        with open(path, 'r') as f:
            self._data = f.read()


        # create list of unique characters and words in the text
        # to be used in the noisy text generation
        self.characters = set(self._data)
        self.characters.remove("\n")
        self.characters = list(self.characters)

        self._data =  self._data.split("\n")
        self.vocab = list(set(self._data))


    def get_clean_data(self):
        return self._data.copy()

    def mess_up_characters(self, p=0.1):
        """Replace each character with a random character with a probability p"""
        d = self.get_clean_data()
        for i in range(len(d)):
            for j in range(len(d[i])):
                if random.random() < p:
                    d[i] = d[i][:j] + random.choice(self.characters) + d[i][j+1:]
        return d


    def mess_up_words(self, p=0.1):
        """Replace each word with a random word with a probability p"""
        d = self.get_clean_data()
        for i in range(len(d)):
            if random.random() < p:
                d[i] = random.choice(self.vocab)
        return d


if __name__ == "__main__":
    dl = DataLoader()
    print("Original text:")
    print(" ".join(dl.get_clean_data()[:200]) + "...\n")


    print("20% character messup:")
    print(" ".join(dl.mess_up_characters(p=0.2)[:200]) + "...\n")

    print("20% word messup:")
    print(" ".join(dl.mess_up_words(p=0.2)[:200]) + "...\n")