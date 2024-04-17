def print_board_state(solution_file, row, col, value, board_state):
    with open(solution_file, "a") as file:
        file.write(f"Successfully placed {value} at position ({row},{col}). Current board state:\n")
        for i in range(9):
            if i % 3 == 0 and i != 0:
                file.write("- - - - - - - - - - - -\n")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    file.write("| ")
                cell_value = str(board_state[i][j]) if board_state[i][j] != 0 else "."
                file.write(cell_value + " " if j < 8 else cell_value + "\n")
        file.write("\n")


# def print_final_board(solution_file, board):
#     with open(solution_file, "a") as file:
#         file.write("Final board configuration:\n")
#         print_current_board(solution_file, board)

# def print_current_board(solution_file, board):
#     for i in range(9):
#         if i % 3 == 0 and i != 0:
#             with open(solution_file, "a") as file:
#                 file.write("- - - - - - - - - - - -\n")
#         for j in range(9):
#             if j % 3 == 0 and j != 0:
#                 with open(solution_file, "a") as file:
#                     file.write("| ")
#             cell_value = str(board[i][j].value) if board[i][j].value != 0 else "."
#             if j == 8:
#                 with open(solution_file, "a") as file:
#                     file.write(cell_value + "\n")
#             else:
#                 with open(solution_file, "a") as file:
#                     file.write(cell_value + " ")
#     with open(solution_file, "a") as file:
#         file.write("\n")
