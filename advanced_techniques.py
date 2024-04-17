def find_xwing(board):
    """
    Áp dụng kỹ thuật Xwing để loại trừ các giá trị khỏi các ô có thể.
    """
    for num in range(1, 10):
        # Tìm các hàng và cột có chứa 2 ô có thể chứa giá trị num
        rows = []
        cols = []
        for i in range(9):
            for j in range(9):
                cell = board[i][j]
                if num in cell.possible_values:
                    if len([k for k in range(9) if num in board[i][k].possible_values]) == 2:
                        rows.append(i)
                    if len([k for k in range(9) if num in board[k][j].possible_values]) == 2:
                        cols.append(j)
        
        # Kiểm tra xem có tạo thành Xwing không
        if len(rows) == 2 and len(cols) == 2:
            # Loại trừ giá trị num khỏi các ô có thể trong hàng và cột không thuộc Xwing
            for i in range(9):
                for j in range(9):
                    if i not in rows or j not in cols:
                        cell = board[i][j]
                        if num in cell.possible_values:
                            cell.possible_values.remove(num)
                            cell.update_possible_values(board)

def find_ywing(board):
    for i in range(9):
        for j in range(9):
            cell1 = board[i][j]
            if len(cell1.possible_values) == 2:
                for k in range(j+1, 9):
                    cell2 = board[i][k]
                    if len(cell2.possible_values) == 2 and cell1.possible_values == cell2.possible_values:
                        for l in range(9):
                            if l != i and l != j and l != k:
                                cell3 = board[l][k]
                                if len(cell3.possible_values) == 2 and cell3.possible_values == cell1.possible_values:
                                    box_x, box_y = k // 3, l // 3
                                    for m in range(box_y * 3, box_y * 3 + 3):
                                        for n in range(box_x * 3, box_x * 3 + 3):
                                            cell = board[m][n]
                                            if cell != cell1 and cell != cell2 and cell != cell3:
                                                for val in cell1.possible_values:
                                                    if val in cell.possible_values:
                                                        cell.possible_values.remove(val)
                                                        cell.update_possible_values(board)

def find_swordfish(board):
    """
    Áp dụng kỹ thuật Swordfish để loại trừ các giá trị khỏi các ô có thể.
    """
    for num in range(1, 10):
        # Tìm các hàng và cột có chứa 3 ô có thể chứa giá trị num
        rows = []
        cols = []
        for i in range(9):
            row_count = len([j for j in range(9) if num in board[i][j].possible_values])
            col_count = len([j for j in range(9) if num in board[j][i].possible_values])
            if row_count == 3:
                rows.append(i)
            if col_count == 3:
                cols.append(i)
        
        # Kiểm tra xem có tạo thành Swordfish không
        if len(rows) == 3 and len(cols) == 3:
            # Loại trừ giá trị num khỏi các ô có thể trong hàng và cột không thuộc Swordfish
            for i in range(9):
                for j in range(9):
                    if i not in rows and j not in cols:
                        cell = board[i][j]
                        if num in cell.possible_values:
                            cell.possible_values.remove(num)
                            cell.update_possible_values(board)

def apply_advanced_techniques(board):
    find_xwing(board)
    find_ywing(board)
    find_swordfish(board)