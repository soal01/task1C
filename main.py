from PIL import Image
import numpy as np
from enum import Enum
from pprint import pprint


def is_black(pixel):
    bound = 10
    return pixel[0] < bound and pixel[1] < bound and pixel[2] < bound


def get_border_coord(data, is_y: bool, is_first: bool) -> int:
    step = 1 if is_first else -1

    i_range = len(data) if is_y else len(data[0])
    i_start = 0 if is_first else i_range - 1
    i_finish = i_range if is_first else 0

    j_range = len(data[0]) if is_y else len(data)
    for i in range(i_start, i_finish, step):
        for j in range(j_range):
            current_cell = data[i][j] if is_y else data[j][i]
            if is_black(current_cell):
                return i


def get_borders(data):
    y1 = get_border_coord(data, True, True)
    x1 = get_border_coord(data, False, True)
    y2 = get_border_coord(data, True, False)
    x2 = get_border_coord(data, False, False)
    return x1, y1, x2, y2


def get_only_field(data) -> list:
    x1, y1, x2, y2 = get_borders(data)
    field = data[y1:y2].copy()
    for i in range(len(field)):
        field[i] = field[i][x1:x2]

    return field


def get_only_cell(field, i, j) -> list:
    cell_size = len(field) // 3  # <-- Привязка к тому, что поле квадратное!
    cell_y_begin = cell_size * i
    cell_y_end = cell_size * (i + 1)

    cell_x_begin = cell_size * j
    cell_x_end = cell_size * (j + 1)

    cell = field[cell_y_begin:cell_y_end]
    for i in range(len(cell)):
        cell[i] = cell[i][cell_x_begin:cell_x_end]

    return cell


def slice_into_cells(data) -> list:
    field = get_only_field(data)
    cells = [[None for _ in range(3)] for __ in range(3)]
    for i in range(3):
        for j in range(3):
            cells[i][j] = get_only_cell(field, i, j)

    return cells


class CellType(Enum):
    NONE = 0
    CROSS = 1
    CIRCLE = 2


def is_empty_center(data):
    offset = 5
    x_center = len(data[0]) // 2
    y_center = len(data) // 2
    for i in range(x_center - offset, x_center + offset):
        for j in range(y_center - offset, y_center + offset):
            if is_black(data[i][j]):
                return False
    return True


def is_empty_cell(data):
    offset = 20  # TODO Magic number
    for i in range(offset, len(data[0]) - offset):
        for j in range(offset,  len(data) - offset):
            if is_black(data[i][j]):
                return False
    return True


def get_cell_type(data) -> CellType:
    center = not is_empty_center(data)
    empty = is_empty_cell(data)
    if center:
        return CellType.CROSS
    elif empty:
        return CellType.NONE
    else:
        return CellType.CIRCLE


def get_primitive_field(data) -> list:
    cells = slice_into_cells(data)
    game_field = [[CellType.NONE for _ in range(3)] for __ in range(3)]

    for i in range(3):
        for j in range(3):
            cell = cells[i][j]
            game_field[i][j] = get_cell_type(cell)

    return game_field


def get_line_winner(line: list) -> CellType:
    expected = line[0]
    if expected == CellType.NONE:
        return CellType.NONE

    for cell in line:
        if cell != expected:
            return CellType.NONE

    return expected


def who_wins(field: list):
    # Проверяем горизонтальные линии
    for index, line in enumerate(field):
        winner = get_line_winner(line)
        if winner != CellType.NONE:
            return winner, index, 0, index, 2

    # Проверяем вертикальные линии
    for row in range(3):
        line = [field[i][row] for i in range(3)]
        winner = get_line_winner(line)
        if winner != CellType.NONE:
            return winner, 0, row, 2, row

    # Проверяем диагонали
    line = [field[i][i] for i in range(3)]
    winner = get_line_winner(line)
    if winner != CellType.NONE:
        return winner, 0, 0, 2, 2

    line = [field[i][2-i] for i in range(3)]
    winner = get_line_winner(line)
    if winner != CellType.NONE:
        return winner, 0, 2, 2, 0

    return CellType.NONE


def get_coords_for_line(pix):
    field = get_primitive_field(pix)
    winner, first_y, first_x, second_y, second_x = who_wins(field)
    x1, y1, x2, y2 = get_borders(pix)
    cell_size = len(get_only_field(pix)) // 3

    return (x1 + cell_size * first_x, y1 + cell_size * first_y), (x1 + cell_size * second_x, y1 + cell_size * second_y)

#
# def draw_vertical_line(data, p1, p2):
#     for i in range(p1[1], p2[1]):
#         data[p1[0]][i] = (255, 0, 0, 255)
#
#
# def draw_horizontal_line(data, p1, p2):
#     for i in range(p1[0], p2[0]):
#         data[i][p1[1]] = (255, 0, 0, 255)
#
#
# def draw_diagonal_line(data, p1, p2):
#     for i in range(p1[0], p2[0]):
#         data[i][i] = (255, 0, 0, 255)
#
#
# def draw_line(data, p1, p2):
#     if (p1[0] == p2[0]):
#         draw_vertical_line(data, p1, p2)
#         return
#
#     if (p1[1] == p2[1]):
#         draw_horizontal_line(data, p1, p2)
#         return
#



def main():
    pic = Image.open("img/image.png")
    pix = np.asarray(pic).tolist()

    field = get_primitive_field(pix)

    pprint(field)
    print()
    pprint(who_wins(field))





if __name__ == '__main__':
    main()



