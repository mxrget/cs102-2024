from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    possible = (x >= 2, y < len(grid[0]) - 2)
    if possible[0] and not possible[1]:
        grid[x - 1][y] = " "
    elif not possible[0] and possible[1]:
        grid[x][y + 1] = " "
    elif possible[0] and possible[1]:
        dir = choice(["up", "right"])
        if dir == "up":
            grid[x - 1][y] = " "
        else:
            grid[x][y + 1] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = list()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == k:
                if i > 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if i < len(grid) - 1 and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if j > 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if j < len(grid[0]) - 1 and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    k = 0
    x, y = exit_coord
    while grid[x][y] == 0:
        k += 1
        grid = make_step(grid, k)

    path = [exit_coord]
    k = int(grid[x][y])
    x, y = exit_coord
    while grid[x][y] != 1 and k > 0:
        if x > 0 and grid[x - 1][y] == k - 1:
            path.append((x - 1, y))
            x -= 1
        if x < len(grid) - 1 and grid[x + 1][y] == k - 1:
            path.append((x + 1, y))
            x += 1
        if y > 0 and grid[x][y - 1] == k - 1:
            path.append((x, y - 1))
            y -= 1
        if y < len(grid[0]) - 1 and grid[x][y + 1] == k - 1:
            path.append((x, y + 1))
            y += 1
        k -= 1

    if len(path) != grid[exit_coord[0]][exit_coord[1]]:
        grid[path[-1][0]][path[-1][1]] = " "
        path.pop()
        x, y = path[-1]
        shortest_path(grid, (x, y))

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows, cols = len(grid), len(grid[0])
    if x in (0, rows - 1) and y in (0, cols - 1):
        return True
    elif x == 0 and grid[x + 1][y] == "■":
        return True
    elif x == rows - 1 and grid[x - 1][y] == "■":
        return True
    elif y == 0 and grid[x][y + 1] == "■":
        return True
    elif y == cols - 1 and grid[x][y - 1] == "■":
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) == 1:
        return (grid, exits[0])
    if any(encircled_exit(grid, exit) for exit in exits):
        return (grid, None)

    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == " ":
                grid[i][j] = 0
    grid[exits[0][0]][exits[0][1]] = 1
    grid[exits[1][0]][exits[1][1]] = 0
    k = 1
    while grid[exits[1][0]][exits[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1
    path_solved = shortest_path(grid, exits[1])

    return (grid, path_solved)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
