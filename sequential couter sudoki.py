from pysat.solvers import Solver

def var(i, j, d):
    return i * 81 + j * 9 + d

# Biến đếm toàn cục cho biến phụ của Sequential Counter
aux_counter = 1000

def add_amo(solver, lits):
    global aux_counter
    n = len(lits)
    if n <= 1: return
    
    # Tạo n-1 biến phụ
    s = [aux_counter + i for i in range(n - 1)]
    aux_counter += (n - 1)
    
    # Ràng buộc Sequential Counter
    solver.add_clause([-lits[0], s[0]])
    for i in range(1, n - 1):
        solver.add_clause([-lits[i], s[i]])
        solver.add_clause([-s[i-1], s[i]])
        solver.add_clause([-s[i-1], -lits[i]])
    solver.add_clause([-s[n-2], -lits[n-1]])

def solve_sudoku_optimized(board):
    global aux_counter
    aux_counter = 1000 
    solver = Solver(name='g3')
    
    #  Mỗi ô có đúng 1 giá trị
    for i in range(9):
        for j in range(9):
            cells = [var(i, j, d) for d in range(1, 10)]
            solver.add_clause(cells) # ALO
            add_amo(solver, cells)   # AMO 

    # Ràng buộc Hàng và Cột
    for k in range(9):
        for d in range(1, 10):
            row_lits = [var(k, j, d) for j in range(9)]
            solver.add_clause(row_lits)
            add_amo(solver, row_lits)
            
            col_lits = [var(i, k, d) for i in range(9)]
            solver.add_clause(col_lits)
            add_amo(solver, col_lits)

    #  Mỗi khối 3x3
    for bi in range(0, 9, 3):
        for bj in range(0, 9, 3):
            for d in range(1, 10):
                block_cells = [var(i, j, d) for i in range(bi, bi+3) for j in range(bj, bj+3)]
                solver.add_clause(block_cells)
                add_amo(solver, block_cells)

    #  Giá trị ban đầu
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                solver.add_clause([var(i, j, board[i][j])])

    if solver.solve():
        model = solver.get_model()
        result = [[0]*9 for _ in range(9)]
        for m in model:
            # Chỉ lấy các biến gốc (m < 1000)
            if 0 < m < 1000:
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


result = solve_sudoku_optimized(board)

print("\nOUTPUT:")
if result:
    for row in result:
        print(' '.join(str(x) for x in row))
    
else:
    print("")