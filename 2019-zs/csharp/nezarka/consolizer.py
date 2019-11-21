import sys

f = open(sys.argv[1], "r")

for line in f.readlines():
    line = line.replace('"', '\\"')

    # remove last newline
    line = line[:-1]
    print('Console.WriteLine("' + line + '");')

f.close()
