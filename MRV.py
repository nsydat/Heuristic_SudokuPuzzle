from advanced_techniques import apply_advanced_techniques
from print_solution import *


import pyautogui as pg
import os
import time
import tracemalloc

class SudokuCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.possible_values = set(range(1, 10))
        self.value = 0

    def update_possible_values(self, board):
        if self.value == 0:
            self.possible_values = set(range(1, 10))
            for i in range(9):
                if board[self.row][i].value != 0:
                    self.possible_values.discard(board[self.row][i].value)
                if board[i][self.col].value != 0:
                    self.possible_values.discard(board[i][self.col].value)
            box_x, box_y = self.col // 3, self.row // 3
            for i in range(box_y * 3, box_y * 3 + 3):
                for j in range(box_x * 3, box_x * 3 + 3):
                    if board[i][j].value != 0:
                        self.possible_values.discard(board[i][j].value)

    def set_value(self, value, board):
        self.value = value
        self.possible_values = set() if value != 0 else set(range(1, 10))
        related_cells = set()
        for i in range(9):
            related_cells.add(board[self.row][i])
            related_cells.add(board[i][self.col])
        box_x, box_y = self.col // 3, self.row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                related_cells.add(board[i][j])
        for cell in related_cells:
            if cell != self:
                cell.update_possible_values(board)

class SudokuBoard:
    def __init__(self):
        self.board = [[SudokuCell(i, j) for j in range(9)] for i in range(9)]
        self.result_board = None
        self.steps = []
        self.solution_file = os.path.join(os.path.dirname(os.path.realpath('__file__')), "solution.txt")

    def initialize_board(self):
        print("Please enter the initial Sudoku board (use 0 for empty cells):")
        board_data = []
        for i in range(9):
            row = [int(x) for x in input(f"Row {i+1}: ").split()]
            board_data.append(row)

        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                cell.value = board_data[i][j]

        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                cell.update_possible_values(self.board)

        self.apply_advanced_techniques()

    def solve_by_mrv(self):
        with open(self.solution_file, "w") as file:
            file.write("Solving Sudoku using MRV...\n")

        if self.backtrack_mrv():
            self.result_board = [[cell.value for cell in row] for row in self.board]
            return True
        else:
            return False

    def backtrack_mrv(self):
        empty_cell = self.find_least_possible_values()
        if not empty_cell:
            return True

        row, col = empty_cell.row, empty_cell.col
        for value in empty_cell.possible_values:
            empty_cell.set_value(value, self.board)
            board_state = tuple(tuple(cell.value if cell.value != 0 else 0 for cell in row) for row in self.board)
            self.steps.append((row, col, value, board_state))
            if self.backtrack_mrv():
                return True
            self.steps.pop()
            empty_cell.set_value(0, self.board)

        return False

    def find_least_possible_values(self):
        min_possible_values = float('inf')
        min_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == 0:
                    num_possible_values = len(self.board[i][j].possible_values)
                    if num_possible_values < min_possible_values:
                        min_possible_values = num_possible_values
                        min_cells = [(i, j)]
                    elif num_possible_values == min_possible_values:
                        min_cells.append((i, j))

        if len(min_cells) == 1:
            return self.board[min_cells[0][0]][min_cells[0][1]]
        else:
            max_degree_cell = None
            max_degree = 0
            for row, col in min_cells:
                cell = self.board[row][col]
                degree = self.get_degree(cell, self.board)
                if degree > max_degree:
                    max_degree = degree
                    max_degree_cell = cell
            return max_degree_cell

    def get_degree(self, cell, board):
        degree = 0
        for i in range(9):
            if board[cell.row][i].value != 0:
                degree += 1
            if board[i][cell.col].value != 0:
                degree += 1
        box_x, box_y = cell.col // 3, cell.row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j].value != 0:
                    degree += 1
        return degree

    def apply_advanced_techniques(self):
        apply_advanced_techniques(self.board)

    def print_board_state(self, row, col, value, board_state):
        print_board_state(self.solution_file, row, col, value, board_state)

    def print_solution(self):
        for step in self.steps:
                row, col, value, board_state = step
                self.print_board_state(row, col, value, board_state)

tracemalloc.start()

sudoku_board = SudokuBoard()
sudoku_board.initialize_board()
start_time = time.time()
if sudoku_board.solve_by_mrv():
    sudoku_board.print_solution()
    print("Result Board:")
    for row in sudoku_board.result_board:
        print(row)
    print("---------------------------------------------------------------------------")
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_cost = time.time() - start_time
    print(f"Solution found in {time_cost:.3f} seconds, using {peak / (1024 ** 2):.3f} MB of memory.")
    print("Steps and final board configuration recorded in solution.txt.")
else:
    print("No solution exists.")

# # Display the solution on the screen
# time.sleep(5)

# for i, row in enumerate(sudoku_board.result_board):  
#     for j, num in enumerate(row):
#         pg.press(str(num), interval=0.0001)
#         if j < 8:
#             pg.press('right', presses=1, interval=0.01)
#         else:
#             pg.press('down', presses=1, interval=0.01)
#             pg.press('left', presses=8, interval=0.01)
