# czech chars

CHARS = [
    "a",
    "á",
    "b",
    "c",
    "č",
    "d",
    "ď",
    "e",
    "é",
    "ě",
    "f",
    "g",
    "h",
    "i",
    "í",
    "j",
    "k",
    "l",
    "m",
    "n",
    "ň",
    "o",
    "ó",
    "p",
    "q",
    "r",
    "ř",
    "s",
    "š",
    "t",
    "ť",
    "u",
    "ú",
    "ů",
    "v",
    "w",
    "y",
    "ý",
    "z",
    "ž",
    " ",
    ".",
    ",",
    "?",
    "!",
    ":",
    ";",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ]



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, default="cz_accent_dev.txt")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

        text = text.replace("\n", " ")


        text = "".join(list(map(lambda x: x if x.lower() in CHARS else "", text)))
        text = text.strip().split()

        print(" ".join(text), end="")
