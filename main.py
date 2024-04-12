from advanced_techniques import apply_advanced_techniques

import pyautogui as pg
import os
import time
import sys

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
        self.memory_cost = 0
        self.time_cost = 0
        self.solution_file = os.path.join(os.path.dirname(os.path.realpath('__file__')), "solution.txt")

    def apply_advanced_techniques(self):
        apply_advanced_techniques(self.board)

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

    def solve_sudoku(self):
        self.start_time = time.time()
        initial_memory = sys.getsizeof(self.board)

        with open(self.solution_file, "w") as file:
            file.write("")

        if self.backtrack():
            self.time_cost = time.time() - self.start_time
            final_memory = sys.getsizeof(self.board)
            self.memory_cost = final_memory - initial_memory
            self.result_board = [[cell.value for cell in row] for row in self.board]  
            return True
        else:
            return False

    def backtrack(self):
        empty_cell = self.find_least_possible_values()
        if empty_cell is None:
            self.print_final_board()  
            return True

        row, col = empty_cell.row, empty_cell.col
        for value in empty_cell.possible_values:
            snapshot = list(empty_cell.possible_values)  
            empty_cell.set_value(value, self.board)
            self.print_board_step(row, col, value, snapshot)
            if self.backtrack():
                return True
            empty_cell.set_value(0, self.board)

        return False

    def find_least_possible_values(self):
        min_possible_values = float('inf')
        min_cell = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == 0 and len(self.board[i][j].possible_values) < min_possible_values:
                    min_possible_values = len(self.board[i][j].possible_values)
                    min_cell = self.board[i][j]
        return min_cell

    def print_board_step(self, row, col, value, possible_values):
        with open(self.solution_file, "a") as file:
            file.write(f"Choosing {value} from list of possible values {possible_values} at position ({row},{col}).\n")
            file.write("Board state after setting this value:\n")
            self.print_current_board(file)

    def print_current_board(self, file):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                file.write("- - - - - - - - - - - -\n")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    file.write("| ")
                cell_value = str(self.board[i][j].value) if self.board[i][j].value != 0 else "."
                if j == 8:
                    file.write(cell_value + "\n")
                else:
                    file.write(cell_value + " ")
        file.write("\n")

    def print_final_board(self):
        with open(self.solution_file, "a") as file:
            file.write("Final board configuration:\n")
            self.print_current_board(file)

sudoku_board = SudokuBoard()
sudoku_board.initialize_board()  
if sudoku_board.solve_sudoku():
    
    print("Result Board:")
    for row in sudoku_board.result_board:
        print(row)
    print("---------------------------------------------------------------------------")
    print(f"Solution found in {sudoku_board.time_cost:.2f} seconds, using {sudoku_board.memory_cost} bytes of memory.") 
    print("Steps and final board configuration recorded in solution.txt.")
else:
    print("No solution exists.")

# Display the solution on the screen
time.sleep(5)

for i, row in enumerate(sudoku_board.result_board):  
    for j, num in enumerate(row):
        pg.press(str(num), interval=0.0001)
        if j < 8:
            pg.press('right', presses=1, interval=0.01)
        else:
            pg.press('down', presses=1, interval=0.01)
            pg.press('left', presses=8, interval=0.01)
