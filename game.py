# game.py

ROWS, COLS = 8, 8

# 色はRGBタプルで定義（main.py側と同じにする）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 盤面の初期化（Noneは空きマス）
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

def init_board():
    """盤面を初期配置にセット"""
    center = ROWS // 2
    board[center - 1][center - 1] = WHITE
    board[center - 1][center]     = BLACK
    board[center][center - 1]     = BLACK
    board[center][center]         = WHITE

def get_flippable_discs(row, col, color):
    """
    指定のマス(row,col)にcolorの駒を置くとき、
    挟んで裏返せる相手の駒の座標リストを返す。
    置けない場合は空リストを返す。
    """
    if board[row][col] is not None:
        return []

    opponent = WHITE if color == BLACK else BLACK
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    flippable = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        discs_to_flip = []
        # 相手の駒を連続して挟む場合
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == opponent:
            discs_to_flip.append((r, c))
            r += dr
            c += dc
        # 最後に自分の駒があるかチェック
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color:
            flippable.extend(discs_to_flip)

    return flippable

def get_legal_moves(color):
    """
    colorが合法手として駒を置けるマスのリストを返す。
    """
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if get_flippable_discs(row, col, color):
                moves.append((row, col))
    return moves

def place_disc(row, col, color):
    """
    指定のマスに駒を置き、挟んだ駒をひっくり返す処理。
    （メインの処理側で裏返しアニメーションを使う場合は
    ひっくり返す座標だけ返す設計でもよい）
    """
    flippable = get_flippable_discs(row, col, color)
    if not flippable:
        return False  # 置けない場所

    board[row][col] = color
    for r, c in flippable:
        board[r][c] = color
    return True
