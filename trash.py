def read_field(filename):
    with open(filename) as file:
        data = list(map(lambda x: list(x), file.read().split('\n')))
        return data


def flip_field(data):
    newdata = []
    for r in range(10):
        newdata.append([data[l][r] for l in range(10)])
    return newdata


def find_ships(ordata):
    data = ordata[:]
    ships = {1: [], 2: [], 3: [], 4: []}
    for l in range(10):
        for r in range(7):
            if "".join(data[l][r:r+4]) == '****':
                ships[4].append([(l, r), (l, r+1), (l, r+2), (l, r+3)])
                data[l] = data[l][:r] + list('____') + data[l][r+4:]
        for r in range(8):
            if "".join(data[l][r:r+3]) == '***':
                ships[3].append([(l, r), (l, r+1), (l, r+2)])
                data[l] = data[l][:r] + list('___') + data[l][r+3:]
        for r in range(9):
            if "".join(data[l][r:r+2]) == '**':
                ships[2].append([(l, r), (l, r+1)])
                data[l] = data[l][:r] + list('__') + data[l][r+2:]
        if l == 0:
            for r in range(10):
                if data[l][r] == '*' and data[l+1][r] == '_':
                    ships[1].append((l, r))
        elif l == 9:
            for r in range(10):
                if data[l][r] == '*' and data[l-1][r] == '_':
                    ships[1].append((l, r))
        else:
            for r in range(10):
                if data[l][r] == '*' and data[l-1][r] == data[l+1][r] == '_':
                    ships[1].append((l, r))
    data = flip_field(ordata)
    for l in range(10):
        for r in range(7):
            if ''.join(data[l][r:r+4]) == '****':
                ships[4].append([(r, l), (r+1, l), (r+2, l), (r+3, l)])
                data[l] = data[l][:r] + list('____') + data[l][r+4:]
        for r in range(8):
            if ''.join(data[l][r:r+3]) == '***':
                ships[3].append([(r, l), (r+1, l), (r+2, l)])
                data[l] = data[l][:r] + list('___') + data[l][r+3:]
        for r in range(9):
            if ''.join(data[l][r:r+2]) == '**':
                ships[2].append([(r, l), (r+1, l)])
                data[l] = data[l][:r] + list('__') + data[l][r+2:]
    return ships


def check_ship(data, dot):
    """
    list(list), tuple(int) -> int
    input - field and dot coordinates
    output - size of ship or 0 if empty
    """
    ships = find_ships(data)
    for size in ships:
        if dot in ships[size]:
                return size
        for ship in ships[size]:
            if dot in ship:
                return size
    return 0


def is_valid(filename):
    with open(filename) as file:
        line = file.read().replace('\n', '')
        if line.count('_') + line.count('*') + line.count('X') != 100:
            return False
        data = read_field(filename)
        if len(data) != 10:
            return False
        for ln in data:
            if len(ln) != 10:
                return False
        ships = find_ships(data)
        if len(ships[1]) != 4 or len(ships[2]) != 3 or len(ships[3]) != 2 or\
           len(ships[4]) != 1:
            return False
    return True


def field_to_str(data):
    field = '\n'.join(list(map(lambda x: ''.join(x), data)))
    return field

# _____________________________________________________________________________________
import random


def downcheck(number):
    if number >= 0:
        return number
    return 0


def cut(field, up, down, left, right):
    field = field[:downcheck(up)] + list(map(lambda x: x[:downcheck(left)] + ['N']*(right - left - 1) + x[right:],
                                             field[downcheck(up):down])) + field[down:]
    return field



def generate():
    # Generate fields
    field = list(map(lambda x: list(x), ['__________'] * 10))
    pos3h = [list(range(8))] * 10
    pos3v = [list(range(10))] * 8
    pos2h = [list(range(9))] * 10
    pos2v = [list(range(10))] * 9

    # Place size 4 ship
    if random.randint(0, 1):
        column4 = random.randrange(7)
        line4 = random.randrange(10)
        field[line4][column4: column4 + 4] = '****'
        pos3h = cut(pos3h, line4 - 1, line4 + 2, column4 - 3, column4 + 5)
        pos3v = cut(pos3v, line4 - 3, line4 + 2, column4 - 1, column4 + 5)
        pos2h = cut(pos2h, line4 - 1, line4 + 2, column4 - 2, column4 + 5)
        pos2v = cut(pos2v, line4 - 2, line4 + 2, column4 - 1, column4 + 5)
    else:
        line4 = random.randrange(7)
        column4 = random.randrange(10)
        for l in range(line4, line4 + 4):
            field[l][column4] = '*'
        pos3h = cut(pos3h, line4 - 1, line4 + 5, column4 - 3, column4 + 2)
        pos3v = cut(pos3v, line4 - 3, line4 + 5, column4 - 1, column4 + 2)
        pos2h = cut(pos2h, line4 - 1, line4 + 5, column4 - 2, column4 + 2)
        pos2v = cut(pos2v, line4 - 2, line4 + 5, column4 - 1, column4 + 2)

    # Place size 3 ships
    for i in range(2):
        if random.randint(0, 1):
            while True:
                line3 = random.randrange(10)
                if pos3h[line3] != ['N']*8:
                    column3 = random.choice(pos3h[line3])
                    if column3 != 'N':
                        break
            field[line3][column3: column3 + 3] = '***'
            pos3h = cut(pos3h, line3 - 1, line3 + 2, column3 - 3, column3 + 4)
            pos3v = cut(pos3v, line3 - 3, line3 + 2, column3 - 1, column3 + 4)
            pos2h = cut(pos2h, line3 - 1, line3 + 2, column3 - 2, column3 + 4)
            pos2v = cut(pos2v, line3 - 2, line3 + 2, column3 - 1, column3 + 4)
        else:
            while True:
                line3 = random.randrange(8)
                if pos3v[line3] != ['N']*10:
                    column3 = random.choice(pos3v[line3])
                    if column3 != 'N':
                        break
            for l in range(line3, line3 + 3):
                field[l][column3] = '*'
            pos3h = cut(pos3h, line3 - 1, line3 + 4, column3 - 3, column3 + 2)
            pos3v = cut(pos3v, line3 - 3, line3 + 4, column3 - 1, column3 + 2)
            pos2h = cut(pos2h, line3 - 1, line3 + 4, column3 - 2, column3 + 2)
            pos2v = cut(pos2v, line3 - 2, line3 + 4, column3 - 1, column3 + 2)

    # Place size 2 ships:

    for i in range(3):
        if random.randint(0, 1):
            while True:
                line2 = random.randrange(10)
                if pos2h[line2] != ['N']*9:
                    column2 = random.choice(pos2h[line2])
                    if column2 != 'N':
                        break
            field[line2][column2: column2 + 2] = '**'
            pos2h = cut(pos2h, line3 - 1, line3 + 2, column3 - 2, column3 + 3)
            pos2v = cut(pos2v, line3 - 2, line3 + 2, column3 - 1, column3 + 3)
        else:
            while True:
                line2 = random.randrange(9)
                if pos2v[line2] != ['N']*10:
                    column2 = random.choice(pos2v[line2])
                    if column2 != 'N':
                        break
            for l in range(line2, line2 + 2):
                field[l][column2] = '*'
            pos2h = cut(pos2h, line3 - 1, line3 + 3, column3 - 2, column3 + 2)
            pos2v = cut(pos2v, line3 - 2, line3 + 3, column3 - 1, column3 + 2)

    return field


print('\n'.join(list(map(lambda x: ' '.join(x), (generate())))))

