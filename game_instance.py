import pygame as pg, numpy as np, random as rnd, math


class GameInstance:
    # "Статические" поля
    board_init = [[0, 0, -1, -1, -1, 0, 0], \
                  [0, 0, 0, -1, 0, 0, 0], \
                  [-1, 0, +1, +1, +1, 0, -1], \
                  [-1, -1, +1, +2, +1, -1, -1], \
                  [-1, 0, +1, +1, +1, 0, -1], \
                  [0, 0, 0, -1, 0, 0, 0], \
                  [0, 0, -1, -1, -1, 0, 0]]
    board_init_sc = [[0, 0, 0, -1, 0, 0, 0], \
                     [0, 0, 0, -1, 0, 0, 0], \
                     [0, 0, 0, +1, 0, 0, 0], \
                     [-1, -1, +1, +2, +1, -1, -1], \
                     [0, 0, 0, +1, 0, 0, 0], \
                     [0, 0, 0, -1, 0, 0, 0], \
                     [0, 0, 0, -1, 0, 0, 0]]
    board_init_11 = [[0, 0, 0, -1, -1, -1, -1, -1, 0, 0, 0], \
                     [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], \
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                     [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1], \
                     [-1, 0, 0, 0, 1, 1, 1, 0, 0, 0, -1], \
                     [-1, -1, 0, 1, 1, 2, 1, 1, 0, -1, -1], \
                     [-1, 0, 0, 0, 1, 1, 1, 0, 0, 0, -1], \
                     [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1], \
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                     [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], \
                     [0, 0, 0, -1, -1, -1, -1, -1, 0, 0, 0]]
    turn_init = 1  # Первыми ходят атакующие
    victory_reason_init = None  # Причина победы

    def __init__(self):
        self.board = [[0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, +1, 0, 0, 0], \
                      [-1, -1, +1, +2, +1, -1, -1], \
                      [0, 0, 0, +1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0]]
        self.turn = GameInstance.turn_init
        self.victory_reason = GameInstance.victory_reason_init

    def new_game(self):
        self.board = [[0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, +1, 0, 0, 0], \
                      [-1, -1, +1, +2, +1, -1, -1], \
                      [0, 0, 0, +1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0], \
                      [0, 0, 0, -1, 0, 0, 0]]
        self.turn = GameInstance.turn_init
        self.victory_reason = GameInstance.victory_reason_init

    def get_current_setup(self):
        attackers_squares = []
        defenders_squares = []
        kings_squares = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == -1:
                    attackers_squares.append((i + 1, j + 1))
                elif self.board[i][j] == 1:
                    defenders_squares.append((i + 1, j + 1))
                elif self.board[i][j] == 2:
                    kings_squares.append((i + 1, j + 1))
        return (attackers_squares, defenders_squares, kings_squares)

    def get_current_turn(self):
        return self.turn

    def get_victory_reason(self):
        return self.victory_reason

    # Возвращает индексы соседних со square квадратов
    # (может вернуть индексы, которых не существует на поле)
    def get_adjanced_squares(self, square):
        return (
        (square[0] + 1, square[1]), (square[0] - 1, square[1]), (square[0], square[1] + 1), (square[0], square[1] - 1))

    # Является ли square стеной ("квадратом", находящимся за пределами доски, но граничащим с каким-либо реальным квадратом)
    def is_wall(self, square):
        # range(len(self.board)) == (0, 1, 2, 3, 4, 5, 6)
        return True if (square[0] == -1 and square[1] in range(len(self.board))) \
                       or (square[0] == len(self.board) and square[1] in range(len(self.board))) \
                       or (square[0] in range(len(self.board)) and square[1] == -1) \
                       or (square[0] in range(len(self.board)) and square[1] == len(self.board)) else False

    def is_corner(self, square):
        return True if square in ((0, 0), (0, len(self.board) - 1), (len(self.board) - 1, 0),
                                  (len(self.board) - 1, len(self.board) - 1)) else False

    def is_thone(self, square):
        return True if square == (math.floor(len(self.board) / 2), math.floor(len(self.board) / 2)) else False

    # Является ли квадрат square враждебным по отношению к фигуре target
    def is_hostile(self, target, square):
        if target == 2:
            # Если фигура - король, то враждебными будут углы, трон, стены и фигуры другого игрока
            return True if self.is_corner(square) or self.is_thone(square) or self.is_wall(square) or (
                        self.board[square[0]][square[1]] * target < 0) else False
        elif target == -1:
            # Если атакующий - углы, трон и фигуры другого игрока
            return True if self.is_corner(square) or self.is_thone(square) or (
                        not self.is_wall(square) and self.board[square[0]][square[1]] * target < 0) else False
        else:
            # Если защитник - углы и фигуры другого игрока
            return True if self.is_corner(square) or (
                        not self.is_wall(square) and self.board[square[0]][square[1]] * target < 0) else False

    # Захвачена ли фигура в квадрате square (координаты от 0 до 6)
    # init_square - квадрат, в который на этом ходу передвинулась фигура
    #    (нужно для корректного определения захвата защитников, которые до этого самостоятельно
    #     переместились в квадрат между атакующими, и поэтому не были удалены)
    def is_trapped(self, square, init_square):
        try:
            initiator = self.board[init_square[0]][init_square[1]]
            target = self.board[square[0]][square[1]]
        except:
            return False

        # Если фигура - король, и при этом ход совершил НЕ защитник
        if target == 2 and initiator < 0:

            adjanced = self.get_adjanced_squares(square)
            trapped = True  # По умолчанию считаем захваченным
            friendly_adj = 0  # Количество защитников, соседствующих с квадратом (для захвата короля допускается не более 1)

            for s in adjanced:
                if (not self.is_wall(s) and self.board[s[0]][s[1]] > 0):
                    friendly_adj += 1
                    if friendly_adj > 1:
                        trapped = False
                        break
                elif not self.is_hostile(target, s):
                    trapped = False
                    break

            return trapped

        # Если в клетке есть вражеская фигура, но это не король
        elif initiator * target < 0:

            delta = (square[0] - init_square[0], square[1] - init_square[1])
            square = (square[0] + delta[0], square[1] + delta[1])

            return True if self.is_hostile(target, square) else False

        # Если клетка пуста
        else:
            return False

    # Список квадратов (1-7), в которые можно совершить ход из квадрата square (1-7)
    def get_list_of_valid_moves(self, normal_square):

        square = (normal_square[0] - 1, normal_square[1] - 1)
        piece = self.board[square[0]][square[1]]
        # print(piece)

        valid_moves = []

        i = 1
        while not (self.is_wall((square[0] + i, square[1]))) and self.board[square[0] + i][square[1]] == 0:
            current_normal_square = (normal_square[0] + i, normal_square[1])
            current_square = (square[0] + i, square[1])
            if piece == 2 or ((not self.is_thone(current_square)) and (not self.is_corner(current_square))):
                valid_moves.append(current_normal_square)
            i += 1
        i = -1
        while not (self.is_wall((square[0] + i, square[1]))) and self.board[square[0] + i][square[1]] == 0:
            current_normal_square = (normal_square[0] + i, normal_square[1])
            current_square = (square[0] + i, square[1])
            if piece == 2 or ((not self.is_thone(current_square)) and (not self.is_corner(current_square))):
                valid_moves.append(current_normal_square)
            i -= 1
        i = 1
        while not (self.is_wall((square[0], square[1] + i))) and self.board[square[0]][square[1] + i] == 0:
            current_normal_square = (normal_square[0], normal_square[1] + i)
            current_square = (square[0], square[1] + i)
            if piece == 2 or ((not self.is_thone(current_square)) and (not self.is_corner(current_square))):
                valid_moves.append(current_normal_square)
            i += 1
        i = -1
        while not (self.is_wall((square[0], square[1] + i))) and self.board[square[0]][square[1] + i] == 0:
            current_normal_square = (normal_square[0], normal_square[1] + i)
            current_square = (square[0], square[1] + i)
            if piece == 2 or ((not self.is_thone(current_square)) and (not self.is_corner(current_square))):
                valid_moves.append(current_normal_square)
            i -= 1

        return valid_moves

    def move(self, begin_square, end_square):
        if self.victory_reason is not None:
            raise Exception('this game is over')

        # Для удобства "человеческую" индексацию (от 1 до 7) помещаем в переменные normal_begin_square и normal_end_square,
        # а "массивную" (от 0 до 6) перезаписываем в begin_square и end_square
        normal_begin_square = (begin_square[0], begin_square[1])
        normal_end_square = (end_square[0], end_square[1])
        begin_square = (begin_square[0] - 1, begin_square[1] - 1)
        end_square = (end_square[0] - 1, end_square[1] - 1)

        # Проверяем, допустим ли ход
        if not (normal_end_square in self.get_list_of_valid_moves(normal_begin_square)):
            raise Exception('could not move from square (%d, %d) to (%d, %d)' % (
            normal_begin_square[0], normal_begin_square[1], normal_end_square[0], normal_end_square[1]))

        # Выполнение передвижения фигуры
        self.board[end_square[0]][end_square[1]] = self.board[begin_square[0]][begin_square[1]]
        self.board[begin_square[0]][begin_square[1]] = 0
        if self.board[end_square[0]][end_square[1]] == 2 and self.is_corner(end_square):
            self.victory_reason = 1

        # Удаляем захваченные фигуры
        removed_pieces = []
        for s in self.get_adjanced_squares(end_square):
            if self.is_trapped(s, end_square):
                # print('Trapped (%d, %d)' % s)
                if self.board[s[0]][s[1]] == 2:  # Если захвачен король, не удаляем его с доски, а просто завершаем игру
                    self.victory_reason = -1
                    continue
                else:
                    self.board[s[0]][s[1]] = 0
                    removed_pieces.append((s[0] + 1, s[1] + 1))
        # else:
        # print('Not trapped: (%d, %d)' % s)

        # Проверяем, остались ли у оппонента фигуры
        opponent_has_pieces = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] * self.turn < 0:
                    opponent_has_pieces = True
        if not opponent_has_pieces and self.victory_reason is None:
            self.victory_reason = 2 * self.turn
        elif self.victory_reason is None:
            # Проверяем, не оказались ли фигуры оппонента полностью окружены
            opponents_valid_moves = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] * self.turn < 0:
                        for m in self.get_list_of_valid_moves((i + 1, j + 1)):
                            opponents_valid_moves.append(m)
            # print(opponents_valid_moves)
            if len(opponents_valid_moves) == 0:
                self.victory_reason = 3 * self.turn

        # Передаем ход следующему игроку, если игра не завершена
        if self.victory_reason is None:
            self.turn *= -1

        return (removed_pieces, self.turn, self.victory_reason)
