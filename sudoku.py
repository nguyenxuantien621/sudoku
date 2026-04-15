
from pysat.solvers import Solver

def var(i, j, d):
    return i * 81 + j * 9 + d

def solve_sudoku(board):
    solver = Solver(name='g3') # Glucose 3
    
    # Mỗi ô có đúng 1 giá trị
    for i in range(9):
        for j in range(9):
            # ALO
            solver.add_clause([var(i, j, d) for d in range(1, 10)])
            # AMO
            for d1 in range(1, 10):
                for d2 in range(d1 + 1, 10):
                    solver.add_clause([-var(i, j, d1), -var(i, j, d2)])
    
   # Hàng và cột
    for k in range(9):
        for d in range(1, 10):
            # ALO
            solver.add_clause([var(k, j, d) for j in range(9)])
            solver.add_clause([var(i, k, d) for i in range(9)])
            # AMO
            for m in range(9):
                for n in range(m + 1, 9):
                    solver.add_clause([-var(k, m, d), -var(k, n, d)]) 
                    solver.add_clause([-var(m, k, d), -var(n, k, d)]) 

    # Mỗi khối 3x3
    for bi in range(0, 9, 3):
        for bj in range(0, 9, 3):
            for d in range(1, 10):                                    
                cells = [var(i, j, d) for i in range(bi, bi + 3) for j in range(bj, bj + 3)]
                solver.add_clause(cells) # ALO
                for idx1 in range(9):
                    for idx2 in range(idx1 + 1, 9):
                        solver.add_clause([-cells[idx1], -cells[idx2]]) # AMO

    # Khởi tạo giá trị ban đầu
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                solver.add_clause([var(i, j, board[i][j])])

    if solver.solve():
        model = solver.get_model()
        result = [[0]*9 for _ in range(9)]

        for m in model:
            if m > 0:
                # Chuyển ngược từ ID về i, j, d
                m_val = m - 1
                d = (m_val % 9) + 1
                j = (m_val // 9) % 9
                i = (m_val // 81)
                result[i][j] = d
        return result
    return None

# Input
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("INPUT:")
for row in board:
    print(' '.join(str(x) for x in row))


result = solve_sudoku(board)

print("\nOUTPUT:")
if result:
    for row in result:
        print(' '.join(str(x) for x in row))
    
else:
    print("")