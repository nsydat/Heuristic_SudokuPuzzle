import pyautogui as pg
import os
import time
import tracemalloc

from print_solution import *


class SudokuCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.value = 0

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

    def solve_by_dfs(self):
        with open(self.solution_file, "w") as file:
            file.write("Solving Sudoku using Depth-First Search...\n")

        if self.backtrack_dfs():
            self.result_board = [[cell.value for cell in row] for row in self.board]
            return True
        else:
            return False

    def backtrack_dfs(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col].value = num
                board_state = tuple(tuple(cell.value if cell.value != 0 else 0 for cell in row) for row in self.board)
                self.steps.append((row, col, num, board_state))
                if self.backtrack_dfs():
                    return True
                self.steps.pop()
                self.board[row][col].value = 0

        return False


    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == 0:
                    return (i, j)
        return None

    def is_safe(self, row, col, num):
        block_row, block_col = row // 3 * 3, col // 3 * 3
        for k in range(9):
            if self.board[row][k].value == num or self.board[k][col].value == num:
                return False
        for i in range(3):
            for j in range(3):
                if self.board[block_row + i][block_col + j].value == num:
                    return False
        return True
    
    
    def print_board_state(self, row, col, value, board_state):
        print_board_state(self.solution_file, row, col, value, board_state)

    # def print_current_board(self, file):
    #     print_current_board(file, self.board)

    # def print_final_board(self):
    #     print_final_board(self.solution_file, self.board)

    def print_solution(self):
        for step in self.steps:
                row, col, value, board_state = step
                self.print_board_state(row, col, value, board_state)

tracemalloc.start()

sudoku_board = SudokuBoard()
sudoku_board.initialize_board()  
start_time = time.time()

if sudoku_board.solve_by_dfs():
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