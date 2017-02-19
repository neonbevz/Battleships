class Ship:
    def __init__(self, bow=(0, 0), horizontal=True, length=1):
        hit = [False for _ in range(length)]
        self.bow, self.horizontal, self.length, self.__hit = bow, horizontal, length, hit

    def shoot_at(self, tup):
        """
        return:
        0 if not hit
        1 if hit
        2 if hit before
        3 if destroyed
        """
        if self.__hit.count(True) == len(self.__hit):
            return 3
        if self.horizontal:
            relative = tup[1] - self.bow[1]
            if tup[0] == self.bow[0] and 0 <= relative < self.length:
                if not self.__hit[relative]:
                    self.__hit = self.__hit[:relative] + [True] + self.__hit[relative + 1:]
                    if self.__hit.count(True) == len(self.__hit):
                        return 3
                    return 1
                else:
                    return 2
            else:
                return 0
        else:
            relative = tup[0] - self.bow[0]
            if tup[1] == self.bow[1] and 0 <= relative < self.length:
                if not self.__hit[relative]:
                    self.__hit = self.__hit[:relative] + [True] + self.__hit[relative + 1:]
                    if self.__hit.count(True) == len(self.__hit):
                        return 3
                    return 1
                else:
                    return 2
            else:
                return 0


class Field:
    __random = __import__('random')

    @staticmethod
    def __downcheck(number):
        if number >= 0:
            return number
        return 0

    def __asdcut(self, field, up, down, left, right):
        field = field[:self.__downcheck(up)] + list(map(lambda x: x[:self.__downcheck(left)] +
                                                        ['N'] * (right - left - 1) + x[right:],
                                                        field[self.__downcheck(up):down])) + field[down:]
        return field

    @staticmethod
    def __cut(field=(), pos=(), length=0, horizontal=True, targetsize=2, targethor=True):
        field = [list(line) for line in field]
        up = pos[0] - 1 if targethor else pos[0] - targetsize
        down = pos[0] + 2 if horizontal else pos[0] + length + 1
        left = pos[1] - targetsize if targethor else pos[1] - 1
        right = pos[1] + length + 1 if horizontal else pos[1] + 2
        if up < 0:
            up = 0
        if down > len(field):
            down = len(field)
        if right > len(field[0]):
            right = len(field[0])
        if left < 0:
            left = 0
        field = field[:up] + list(map(lambda x: x[:left] + ['N' for _ in range(right - left)]
                                      + x[right:], field[up:down])) + field[down:]
        return field

    def __randompos(self, lst):
        while True:
            lineind = self.__random.randrange(len(lst))
            line = lst[lineind]
            if line != ['N'] * (len(line)):
                for column in self.__random.sample(line, len(line)):
                    if column != 'N':
                        return lineind, column

    def __generate(self):
        # Generate fields
        field = list(map(lambda x: list(x), ['__________'] * 10))
        pos3h = [list(range(8))] * 10
        pos3v = [list(range(10))] * 8
        pos2h = [list(range(9))] * 10
        pos2v = [list(range(10))] * 9

        # Place size 4 ship
        if self.__random.randint(0, 1):
            column4 = self.__random.randrange(7)
            line4 = self.__random.randrange(10)
            self.ship4 = Ship(bow=(line4, column4), horizontal=True, length=4)
            field[line4][column4: column4 + 4] = '****'
            pos3h = self.__cut(field=pos3h, pos=(line4, column4), length=4, horizontal=True, targetsize=3,
                               targethor=True)
            pos3v = self.__cut(field=pos3v, pos=(line4, column4), length=4, horizontal=True, targetsize=3,
                               targethor=False)
            pos2h = self.__cut(field=pos2h, pos=(line4, column4), length=4, horizontal=True, targetsize=2,
                               targethor=True)
            pos2v = self.__cut(field=pos2v, pos=(line4, column4), length=4, horizontal=True, targetsize=2,
                               targethor=False)
        else:
            line4 = self.__random.randrange(7)
            column4 = self.__random.randrange(10)
            self.ship4 = Ship(bow=(line4, column4), horizontal=False, length=4)
            for l in range(line4, line4 + 4):
                field[l][column4] = '*'
            pos3h = self.__cut(field=pos3h, pos=(line4, column4), length=4, horizontal=False, targetsize=3,
                               targethor=True)
            pos3v = self.__cut(field=pos3v, pos=(line4, column4), length=4, horizontal=False, targetsize=3,
                               targethor=False)
            pos2h = self.__cut(field=pos2h, pos=(line4, column4), length=4, horizontal=False, targetsize=2,
                               targethor=True)
            pos2v = self.__cut(field=pos2v, pos=(line4, column4), length=4, horizontal=False, targetsize=2,
                               targethor=False)

        # Place size 3 ships
        for sh in range(2):
            if self.__random.randint(0, 1):
                line3, column3 = self.__randompos(pos3h)
                exec('self.ship3_' + str(sh + 1) + ' = Ship(bow=(' + str(line3) + ', ' + str(column3) + '),\
 horizontal=True, length=3)')
                field[line3][column3: column3 + 3] = '***'
                pos3h = self.__cut(field=pos3h, pos=(line3, column3), length=3, horizontal=True, targetsize=3,
                                   targethor=True)
                pos3v = self.__cut(field=pos3v, pos=(line3, column3), length=3, horizontal=True, targetsize=3,
                                   targethor=False)
                pos2h = self.__cut(field=pos2h, pos=(line3, column3), length=3, horizontal=True, targetsize=2,
                                   targethor=True)
                pos2v = self.__cut(field=pos2v, pos=(line3, column3), length=3, horizontal=True, targetsize=2,
                                   targethor=False)
            else:
                line3, column3 = self.__randompos(pos3v)
                exec('self.ship3_' + str(sh + 1) + ' = Ship(bow=(' + str(line3) + ', ' + str(column3) + '),\
 horizontal=False, length=3)')
                for l in range(line3, line3 + 3):
                    field[l][column3] = '*'
                pos3h = self.__cut(field=pos3h, pos=(line3, column3), length=3, horizontal=False, targetsize=3,
                                   targethor=True)
                pos3v = self.__cut(field=pos3v, pos=(line3, column3), length=3, horizontal=False, targetsize=3,
                                   targethor=False)
                pos2h = self.__cut(field=pos2h, pos=(line3, column3), length=3, horizontal=False, targetsize=2,
                                   targethor=True)
                pos2v = self.__cut(field=pos2v, pos=(line3, column3), length=3, horizontal=False, targetsize=2,
                                   targethor=False)

        # Place size 2 ships:

        for sh in range(3):
            if self.__random.randint(0, 1):
                line2, column2 = self.__randompos(pos2h)
                exec('self.ship2_' + str(sh + 1) + ' = Ship(bow=(' + str(line2) + ', ' + str(column2) + '),\
                                 horizontal=True, length=2)')
                field[line2][column2: column2 + 2] = '**'
                pos2h = self.__cut(field=pos2h, pos=(line2, column2), length=2, horizontal=True, targetsize=2,
                                   targethor=True)
                pos2v = self.__cut(field=pos2v, pos=(line2, column2), length=2, horizontal=True, targetsize=2,
                                   targethor=False)
            else:
                line2, column2 = self.__randompos(pos2v)
                exec('self.ship2_' + str(sh + 1) + ' = Ship(bow=(' + str(line2) + ', ' + str(column2) + '),\
                                                 horizontal=False, length=2)')
                for l in range(line2, line2 + 2):
                    field[l][column2] = '*'
                pos2h = self.__cut(field=pos2h, pos=(line2, column2), length=2, horizontal=False, targetsize=2,
                                   targethor=True)
                pos2v = self.__cut(field=pos2v, pos=(line2, column2), length=2, horizontal=False, targetsize=2,
                                   targethor=False)

    def __init__(self):
        self.__field_wos = [list('__________') for _ in range(10)]
        self.__generate()
        self.ships = (self.ship4, self.ship3_1, self.ship3_2, self.ship2_1, self.ship2_2, self.ship2_3)
        self.__field_ws = self.field_with_ships()

    def field_with_ships(self):
        field = [list('__________') for _ in range(10)]
        for ship in self.ships:
            if ship.horizontal:
                field[ship.bow[0]][ship.bow[1]:ship.bow[1] + ship.length] = ['0' for _ in range(ship.length)]
            else:
                for l in range(ship.length):
                    field[ship.bow[0] + l][ship.bow[1]] = '0'
        for line in range(10):
            for column in range(10):
                if self.__field_wos[line][column] != '_':
                    field[line][column] = self.__field_wos[line][column]
        return field

    def field_without_ships(self):
        return self.__field_wos

    def shoot_at(self, tup):
        for ship in self.ships:
            hit = ship.shoot_at(tup)
            char = '+'
            if hit == 0:
                continue
            elif hit in (1, 3):
                char = 'X'
                break
            elif hit == 2:
                return 2
        self.__field_wos[tup[0]][tup[1]] = char
        if char == '+':
            return 0
        return hit

    @staticmethod
    def tostring(field):
        return '\n'.join(list(map(lambda x: ' '.join(x), field)))


class Player:
    def __init__(self, name):
        self.__name = name


class Game:
    def __init__(self, name1, name2):
        self.__field1 = Field()
        self.__field2 = Field
        self.__player1 = Player(name1)
        self.__player2 = Player(name2)
        self.__current_player = 1

    @staticmethod
    def read_position(pos):
        alph = list('ABCDEFGHIJ')
        return alph.find(pos[1]), int(pos[2])



myfield = Field()
print(myfield.tostring(myfield.field_with_ships()))
