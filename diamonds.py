import json
import time


class Piece:
    number: int = 0
    letter: str = ''
    color: str = ''

    height: int = 0
    width: int = 0
    shape: list = None

    orientations: list = None
    positions: list = None
    translations: list = None

    def __init__(self, number: int, letter: str, color: str, shape: list, options: list):
        self.number = number
        self.letter = letter
        self.color = color

        self.height = len(shape)
        self.width = len(shape[0])
        self.shape = shape

        self.orientations = list()
        for option in options:
            self.orientations.append(self.orientate(option[0], option[1]))

    @staticmethod
    def static(source: list):
        if len(source) == 5:
            return Piece(source[0], source[1], source[2], source[3], source[4])
        else:
            print('Piece is invalid!')
            exit(1)

    def orientate(self, angle: int, flip: bool) -> list:
        if flip:
            source = [[0 for i in range(len(self.shape[0]))] for j in range(len(self.shape))]
            for j in range(len(self.shape)):
                for i in range(len(self.shape[0])):
                    source[j][len(self.shape[0]) - 1 - i] = self.shape[j][i]
        else:
            source = self.shape

        if angle == 90 or angle == -270:
            nh = len(source[0])
            nw = len(source)
            result = [[0 for i in range(nw)] for j in range(nh)]
            for j in range(len(source)):
                for i in range(len(source[0])):
                    result[i][nw - 1 - j] = source[j][i]
        elif angle == 180 or angle == -180:
            nh = len(source)
            nw = len(source[0])
            result = [[0 for i in range(nw)] for j in range(nh)]
            for j in range(len(source)):
                for i in range(len(source[0])):
                    result[nh - 1 - j][nw - 1 - i] = source[j][i]
        elif angle == 270 or angle == -90:
            nh = len(source[0])
            nw = len(source)
            result = [[0 for i in range(nw)] for j in range(nh)]
            for j in range(len(source)):
                for i in range(len(source[0])):
                    result[nh - 1 - i][j] = source[j][i]
        else:
            result = source[:]

        return result

    def position(self, fw: int, fh: int):
        self.positions = list()
        for orientation in self.orientations:
            if fh < len(orientation) or fw < len(orientation[0]):
                continue

            for j in range(fh - len(orientation) + 1):
                for i in range(fw - len(orientation[0]) + 1):
                    position = [[0 for m in range(fw)] for n in range(fh)]
                    for n in range(len(orientation)):
                        for m in range(len(orientation[0])):
                            position[j + n][i + m] = orientation[n][m]
                    self.positions.append(position)
        self.translate()

    def translate(self):
        self.translations = list()
        for position in self.positions:
            translation = list()
            for row in position:
                for value in row:
                    translation.append(value)
            self.translations.append(translation)


class Problem:
    pointer: str = '05-0C-123456789ABC'

    height: int = 12
    width: int = 5
    size: int = 72
    # neighbors: list = None

    pieces: list = None
    cards: list = None
    solutions: list = None

    def __init__(self, width: int, height: int, pieces: list):
        if (len(pieces) > 2) and (len(pieces) < 13) and (width > 2) and (height > 2) and \
                (width * height == 5 * len(pieces)):
            self.width = min(width, height)
            self.height = max(width, height)
            self.size = self.width * self.height + len(pieces)
            self.pointer = '%02X-%02X' % (self.width, self.height) + '-'
            # self.neighbors = list()
            # for j in range(self.height):
            #     for i in range(self.width):
            #         inner = list()
            #         if j > 0:
            #             inner.append(self.width * (j - 1) + i)
            #         if i > 0:
            #             inner.append(self.width * j + (i - 1))
            #         if i < self.width - 1:
            #             inner.append(self.width * j + (i + 1))
            #         if j < self.height - 1:
            #             inner.append(self.width * (j + 1) + i)
            #         self.neighbors.append(inner)
            self.pieces = pieces
            self.solutions = list()
            self.cards = list()
            for count, piece in enumerate(self.pieces):
                self.pointer = self.pointer + '%X' % piece.number
                piece.position(self.width, self.height)
                pointer = [0 for i in range(len(self.pieces))]
                pointer[count] = 1
                for translation in piece.translations:
                    self.cards.append(translation + pointer)
        else:
            print('Problem is invalid!')
            exit(1)

    @staticmethod
    def static(pointer: str):
        if 8 < len(pointer) < 7 + len(pieces_glo):
            width = int(pointer[0:2], 16)
            height = int(pointer[3:5], 16)
            pieces = list()
            for number_hex in pointer[6::]:
                number_dec = int(number_hex, 16) - 1
                if -1 < number_dec < len(pieces_glo):
                    pieces.append(Piece.static(pieces_glo[number_dec]))
            return Problem(width, height, pieces)
        else:
            print('Problem is invalid!')
            exit(1)

    def solve(self, how_many: int = 1, track: bool = False,
              level: int = 0, indices_ext: list = None, cards_ext: list = None, solution_ext: list = None):
        indices_int = list(range(self.width * self.height + len(self.pieces))) if indices_ext is None else indices_ext
        cards_int = self.cards[:] if cards_ext is None else cards_ext
        solution_int = [] if (solution_ext is None) or (level == 0) else solution_ext

        position = indices_int[0]
        indices_int = indices_int[1::]

        positives, negatives = self.filter_by_one_ex(position, 1, cards_int)
        if len(positives) > 0:
            # negatives = self.filter_by_one(position, 0, cards_int)
            for positive in positives:
                indices_sub = list()
                indices_neg = list()
                for index in indices_int:
                    if positive[index] == 1:
                        indices_neg.append(index)
                    else:
                        indices_sub.append(index)
                negatives_sub = self.filter_by_many(indices_neg, 0, negatives)

                if len(negatives_sub) > 0:
                    self.solve(how_many, track, level + 1, indices_sub, negatives_sub, solution_int + [positive])
                    if len(self.solutions) == how_many:
                        return
                else:
                    if len(indices_sub) == 0 and level + 1 == len(self.pieces):
                        self.solutions.append(solution_int + [positive])
                        if track:
                            print(len(self.solutions))
                        if len(self.solutions) == how_many:
                            return

    def filter_by_one(self, position: int, value: int, cards_ext: list = None) -> list:
        cards_int = self.cards[:] if cards_ext is None else cards_ext
        result = list()
        for card in cards_int:
            if card[position] == value:
                result.append(card)
        return result

    def filter_by_one_ex(self, position: int, value: int, cards_ext: list = None) -> (list, list):
        cards_int = self.cards[:] if cards_ext is None else cards_ext
        result_success = list()
        result_failure = list()
        for card in cards_int:
            if card[position] == value:
                result_success.append(card)
            else:
                result_failure.append(card)
        return result_success, result_failure

    def filter_by_many(self, positions: list, value: int, cards_ext: list = None) -> list:
        cards_int = self.cards[:] if cards_ext is None else cards_ext
        result = list()
        for card in cards_int:
            success = True
            for position in positions:
                if not card[position] == value:
                    success = False
                    break
            if success:
                result.append(card)
        return result

    def display_total(self):
        print('--- Total: ' + str(len(self.solutions)) + ' ---')

    def display_all(self):
        self.display_total()
        for i in range(len(self.solutions)):
            self.display_one(i)

    def display_one(self, index: int):
        if -1 < index < len(self.solutions):
            solution = self.solutions[index]
            print('=== Solution ' + str(index + 1) + '/' + str(len(self.solutions)) + ' ===')
            for j in range(self.height):
                row = ''
                for card in solution:
                    letter = ''
                    for number, value in enumerate(card[-len(self.pieces)::]):
                        if value == 1:
                            letter = self.pieces[number].letter
                            break
                    for value in card[self.width * j:self.width * (j + 1)]:
                        row = row + (letter if value == 1 else '\u2219')
                    row = row + '   '
                print(row)

    def display_first(self):
        self.display_one(0)

    def quick(self):
        self.solve(1)
        self.display_first()

    def cheat(self):
        self.load()
        if len(self.solutions) == 0:
            self.solve(1)
        self.display_first()
        self.dump()

    def dump(self):
        dumps = list()
        length = self.size // 4 + (self.size % 4 > 0)
        for solution in self.solutions:
            dump = list()
            for card in solution:
                dump.append('%0*X' % (length, int('0b' + ''.join(map(str, card)), 2)))
            dumps.append(dump)
        library_glo[self.pointer] = dumps

    def load(self):
        if self.pointer in library_glo:
            self.solutions = list()
            loads = library_glo[self.pointer]
            for load in loads:
                solution = list()
                for string_hex in load:
                    card = list()
                    string_bin = bin(int(string_hex, 16))[2::].zfill(self.size)
                    for value in string_bin:
                        card.append(int(value))
                    solution.append(card)
                self.solutions.append(solution)


# P1 = Piece(1, 'O', 'Rose', [[1, 1, 1, 1, 1]],
#            [[0, False], [90, False]])
# P2 = Piece(2, 'Q', 'Orange', [[1, 1, 1, 1], [1, 0, 0, 0]],
#            [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]])
# P3 = Piece(3, 'Y', 'Brown', [[1, 1, 1, 1], [0, 1, 0, 0]],
#            [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]])
# P4 = Piece(4, 'S', 'Black', [[0, 1, 1, 1], [1, 1, 0, 0]],
#            [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]])
# P5 = Piece(5, 'V', 'Dark Blue', [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
#            [[0, False], [90, False], [180, False], [270, False]])
# P6 = Piece(6, 'P', 'Light Blue', [[1, 1, 1], [1, 1, 0]],
#            [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]])
# P7 = Piece(7, 'U', 'Yellow', [[1, 1, 1], [1, 0, 1]],
#            [[0, False], [90, False], [180, False], [270, False]])
# P8 = Piece(8, 'Z', 'Grey', [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
#            [[0, False], [90, False], [0, True], [90, True]])
# P9 = Piece(9, 'R', 'Light Green', [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
#            [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]])
# PA = Piece(10, 'T', 'Dark Green', [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
#            [[0, False], [90, False], [180, False], [270, False]])
# PB = Piece(11, 'W', 'Cherry', [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
#            [[0, False], [90, False], [180, False], [270, False]])
# PC = Piece(12, 'X', 'Red', [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
#            [[0, False]])

with open('pieces.json', 'r') as fp:
    pieces_glo: list = json.load(fp)

with open('library.json', 'r') as fp:
    library_glo: dict = json.load(fp)

with open('problems.json', 'r') as fp:
    problems_glo: dict = json.load(fp)

for group, pointers in problems_glo.items():
    print('--- Group:', group, '---')
    for pointer in pointers:
        problem = Problem.static(pointer)
        problem.cheat()

# T20 = Problem(20, 3, [P1, P2, P3, P4, P5, P6, P7, P8, P9, PA, PB, PC])
TBA = Problem.static('05-0B-123456789AB')
t0 = time.perf_counter()
TBA.cheat()
print('--- Time elapsed: {:.7f} ---'.format(time.perf_counter() - t0))
TBA.display_total()
# print(T20.pointer)
# T20.cheat()

with open('library.json', 'w') as fp:
    json.dump(library_glo, fp)

# dump all pieces to json
# with open('pieces.json', 'w') as fp:
#      json.dump([[1, 'O', 'Rose', [[1, 1, 1, 1, 1]],
#                 [[0, False], [90, False]]],
#                 [2, 'Q', 'Orange', [[1, 1, 1, 1], [1, 0, 0, 0]],
#                 [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]],
#                 [3, 'Y', 'Brown', [[1, 1, 1, 1], [0, 1, 0, 0]],
#                 [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]],
#                 [4, 'S', 'Black', [[0, 1, 1, 1], [1, 1, 0, 0]],
#                 [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]],
#                 [5, 'V', 'Dark Blue', [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
#                 [[0, False], [90, False], [180, False], [270, False]]],
#                 [6, 'P', 'Light Blue', [[1, 1, 1], [1, 1, 0]],
#                 [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]],
#                 [7, 'U', 'Yellow', [[1, 1, 1], [1, 0, 1]],
#                 [[0, False], [90, False], [180, False], [270, False]]],
#                 [8, 'Z', 'Grey', [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
#                 [[0, False], [90, False], [0, True], [90, True]]],
#                 [9, 'R', 'Light Green', [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
#                 [[0, False], [90, False], [180, False], [270, False], [0, True], [90, True], [180, True], [270, True]]],
#                 [10, 'T', 'Dark Green', [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
#                 [[0, False], [90, False], [180, False], [270, False]]],
#                 [11, 'W', 'Cherry', [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
#                 [[0, False], [90, False], [180, False], [270, False]]],
#                 [12, 'X', 'Red', [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
#                 [[0, False]]]], fp)