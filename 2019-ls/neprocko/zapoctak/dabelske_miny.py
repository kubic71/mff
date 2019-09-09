import random

SIZE = 8
N_MINES = 10
TIME_TO_DABEL = 4
DABEL = False

random.seed(42)

def random_grid():
    planted = 0
    grid = [[False for i in range(SIZE)] for j in range(SIZE)]

    while planted < N_MINES:
        x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        if grid[x][y] == False:
            grid[x][y] = True
            planted += 1
    return grid



def inBounds(x, y):
    return x >= 0 and y >= 0 and x < SIZE and y < SIZE

# returns number of surrounding mines
def getNumMinesInfo(mines):
    info = [[0 for i in range(SIZE)] for j in range(SIZE)]
    for x in range(SIZE):
        for y in range(SIZE):
            if mines[x][y]:
                continue

            for xplus in (-1, 0, 1):
                for yplus in (-1, 0, 1):
                    xpos, ypos = x + xplus, y + yplus
                    if inBounds(xpos, ypos) and mines[xpos][ypos]:
                        info[x][y] += 1

    return info


def recursively_uncover(x, y, mines, uncovered, info):
    if not inBounds(x, y):
        return

    print("Uncovering:", x, y)
    if info[x][y] != 0:

        uncovered[x][y] = True
        return

    if not uncovered[x][y]:
        uncovered[x][y] = True
        for xp in (-1, 0, 1):
            for yp in (-1, 0, 1):
                recursively_uncover(x + xp, y + yp, mines, uncovered, info)



def printBoard(mines, uncovered, debug=False):
    info = getNumMinesInfo(mines)

    print("--" + " ".join([chr(code) for code in range(ord("a"),ord("a") + SIZE)]) + "--")
    for y in range(SIZE):
        print(str(y + 1) + "|", end="")
        for x in range(SIZE):
            if debug:
                if mines[x][y]:
                    print("X ", end="")
                else:
                    print(str(info[x][y]) + " ", end="")
            else:
                if uncovered[x][y]:
                    print(str(info[x][y]) + " ", end="")
                else:
                    print("* ", end="")
        print("|")


# try to generate valid mines placement for given info and uncovered state
# by backtracing do/do not place mine on every covered cell

MINE = 1
NOT_MINE = 0
def generate_mines(x, y, uncovered, info, mine_value):
    mine_values = {}
    possible_mines = [(xp, yp) for xp in range(SIZE) for yp in range(SIZE) if not uncovered[xp][yp]]
    possible_mines.remove((x, y))
    mine_values[(x, y)] = mine_value

    success = place_mine(0, possible_mines, mine_values, uncovered, info)
    if success:
        return [[True if ((x, y) in mine_values and mine_values[(x, y)] == MINE) else False for y in range(SIZE)] for x in range(SIZE)]
    return None


def place_mine(i, possible_mines, mine_values, uncovered, info):
    if i == len(possible_mines):
        return True
    x, y = possible_mines[i]

    # randomize the order in which the tree is searched
    first_try = random.choice([NOT_MINE, MINE])

    mine_values[(x, y)] = first_try
    if check(mine_values, uncovered, info):
        success = place_mine(i + 1, possible_mines, mine_values, uncovered, info)
        if success:
            return Tru  e

    mine_values[(x, y)] = 1 - first_try
    if check(mine_values, uncovered, info):
        success = place_mine(i + 1, possible_mines, mine_values, uncovered, info)
        if success:
            return True

    del mine_values[(x, y)]
    return False


def check(mine_values, uncovered, info):
    for x in range(SIZE):
        for y in range(SIZE):
            if uncovered[x][y]:
                incomplete_assignment = False
                surrounding_mines = 0
                for xn, yn in neighbours(x, y):
                    if (xn, yn) in mine_values:
                        surrounding_mines += mine_values[(xn, yn)]
                    else:
                        # some covered cell doesn't have mine assignment yet
                        if not uncovered[xn][yn]:
                            incomplete_assignment = True
                            break

                if incomplete_assignment:
                    continue
                elif surrounding_mines != info[x][y]:
                    return False
    return True


def neighbours(x, y):
    l = []
    for xp in (-1, 0, 1):
        for yp in (-1, 0, 1):
            if xp == 0 and yp == 0:
                continue
            xnew, ynew = x + xp, y + yp
            if inBounds(xnew, ynew):
                l.append((xnew, ynew))
    return l



def play():
    global DABEL

    mines = random_grid()
    uncovered = [[False for i in range(SIZE)] for j in range(SIZE)]

    t = 0
    while True:
        printBoard(mines, uncovered)
        printBoard(mines, uncovered, debug=True)
        choice = input(":")
        try:
            xc, yc = ord(choice[0]) - ord("a"), int(choice[1]) - 1
        except:
            print("Invalid coordinates")
            continue
        if not inBounds(xc, yc):
            continue

        if DABEL:
            print("Dabel!")
            new_mines = generate_mines(xc, yc, uncovered, getNumMinesInfo(mines), MINE)
            if new_mines:
                print("BOOM!")
                mines = new_mines
                printBoard(mines, uncovered)
                printBoard(mines, uncovered, debug=True)
                return
            else:
                mines = generate_mines(xc, yc, uncovered, getNumMinesInfo(mines), NOT_MINE)

        else:
            if mines[xc][yc]:
                print("BOOM!")
                printBoard(mines, uncovered)
                printBoard(mines, uncovered, debug=True)
                return

            t += 1
            if t > TIME_TO_DABEL:
                DABEL = True

        recursively_uncover(xc, yc, mines, uncovered, getNumMinesInfo(mines))






play()






