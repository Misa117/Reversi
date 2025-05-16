# 定数の定義
ROWS, COLS = 8, 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ボードの初期化
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

def init_board():
    center = ROWS // 2
    board[center - 1][center - 1] = WHITE
    board[center - 1][center]     = BLACK
    board[center][center - 1]     = BLACK
    board[center][center]         = WHITE

def get_flippable_discs(row, col, color):
    if board[row][col] is not None:
        return []
    opponent = WHITE if color == BLACK else BLACK
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0),  (1, 1)]
    result = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        line = []
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == opponent:
            line.append((r, c))
            r += dr
            c += dc
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color:
            result.extend(line)
    return result

def place_disc(row, col, color):
    flipped = get_flippable_discs(row, col, color)
    if not flipped:
        return False
    board[row][col] = color
    for r, c in flipped:
        board[r][c] = color
    return True

def get_legal_moves(color):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if get_flippable_discs(row, col, color):
                moves.append((row, col))
    return moves
