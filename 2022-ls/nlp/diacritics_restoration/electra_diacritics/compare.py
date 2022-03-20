def number_of_correct_chars(orig: str, pred: str):
    assert len(orig) == len(pred)

    correct = 0
    for o, p in zip(orig, pred):
        if o == p:
            correct += 1

    return correct

def number_of_correct_words(orig: str, pred: str):
    orig, pred = orig.split(), pred.split()
    if len(orig) != len(pred):
        print(orig)
        print(pred)
        print(len(orig), len(pred))

    assert len(orig) == len(pred), (orig, pred)

    correct = 0
    for o, p in zip(orig, pred):
        if o == p:
            correct += 1

    return correct, len(orig)

def comapare_files(correct_fn: str, pred_fn: str):
    with open(correct_fn, "r") as f_correct, open(pred_fn, "r") as f_pred:
        correct_lines = f_correct.readlines()
        pred_lines = f_pred.readlines()

    assert len(correct_lines) == len(pred_lines)

    correct_words = 0
    correct_chars = 0
    total_words = 0
    total_chars = 0
    for c, p in zip(correct_lines, pred_lines):
        c, p = c.strip(), p.strip()
        correct_chars += number_of_correct_chars(c, p)
        correct_words += number_of_correct_words(c, p)[0]
        total_chars += len(c)
        total_words += len(c.split())

    return {"correct_chars": correct_chars, "correct_words": correct_words, "total_chars": total_chars, "total_words": total_words}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--correct-file', type=str, default="data/diacritics-etest.txt")
    parser.add_argument('--pred-file', type=str)

    args = parser.parse_args()

    comparison = comapare_files(args.correct_file, args.pred_file)

    print(f"Character accuracy: {comparison['correct_chars']}/{comparison['total_chars']} = {comparison['correct_chars']/comparison['total_chars']}")
    print(f"Word accuracy: {comparison['correct_words']}/{comparison['total_words']} = {comparison['correct_words']/comparison['total_words']}")

