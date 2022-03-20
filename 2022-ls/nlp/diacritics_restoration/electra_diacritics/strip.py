from train import strip_map


def strip_string(string: str):
    out = []

    for char in string:
        cl = char.lower()
        if cl in strip_map:
            if char.isupper():
                out.append(strip_map[cl].upper())
            else:
                out.append(strip_map[cl])
        else:
            out.append(char)

    return "".join(out)

def strip_file(file_input: str, file_output: str):
    with open(file_input, "r") as f_in, open(file_output, "w") as f_out:
        content = f_in.read()
        f_out.write(strip_string(content))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    strip_file(args.input, args.output)