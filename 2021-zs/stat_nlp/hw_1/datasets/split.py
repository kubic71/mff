import argparse

# read path from command line argument
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="path to file", required=True, type=str)
args = parser.parse_args()
path = args.path

with open(path, 'r') as f:
    data = f.read().strip().split("\n")

# strip the last 20000 lines and call them test data
test_data = data[-20000:]
data = data[:-20000]

# then take off the last 40000 lines from what remains and call them heldout data
heldout_data = data[-40000:]
train = data[:-40000]

dataset_name = path.split(".")[0]

# save train, heldout and test data to separate files

# save train data
with open(dataset_name + "_train.txt", 'w') as f:
    f.write("\n".join(train))

# save heldout data
with open(dataset_name + "_heldout.txt", 'w') as f:
    f.write("\n".join(heldout_data))

# save test data
with open(dataset_name + "_test.txt", 'w') as f:
    f.write("\n".join(test_data))
