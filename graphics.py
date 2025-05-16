import pygame
import os

# 画像の読み込み
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'images')

board_texture = pygame.image.load(os.path.join(ASSETS_DIR, 'board_texture.jpg'))
frame_texture = pygame.image.load(os.path.join(ASSETS_DIR, 'frame_texture.jpg'))
black_disc_image = pygame.image.load(os.path.join(ASSETS_DIR, 'black_disc.png'))
white_disc_image = pygame.image.load(os.path.join(ASSETS_DIR, 'white_disc.png'))

# 盤面の描画
def draw_board(screen, CELL_SIZE, margin=40):
    # 外枠の描画
    frame_texture_scaled = pygame.transform.scale(frame_texture, screen.get_size())
    screen.blit(frame_texture_scaled, (0, 0))

    # 盤面の描画
    board_width = CELL_SIZE * 8
    board_height = CELL_SIZE * 8
    board_surface = pygame.transform.scale(board_texture, (board_width, board_height))
    screen.blit(board_surface, (margin, margin))

    # グリッド線の描画
    for x in range(8):
        for y in range(8):
            rect = pygame.Rect(
                margin + x * CELL_SIZE,
                margin + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

# 石の描画
def draw_discs(screen, board, CELL_SIZE, margin=40):
    for row in range(8):
        for col in range(8):
            color = board[row][col]
            if color:
                x = margin + col * CELL_SIZE
                y = margin + row * CELL_SIZE
                disc_image = black_disc_image if color == (0, 0, 0) else white_disc_image
                disc_scaled = pygame.transform.scale(disc_image, (CELL_SIZE - 10, CELL_SIZE - 10))
                screen.blit(disc_scaled, (x + 5, y + 5))

# メッセージの表示（パスのとき以外、盤面を再描画しない）
def show_message(screen, text, WIDTH, HEIGHT, redraw_background=False, CELL_SIZE=None, board=None):
    if redraw_background and CELL_SIZE and board:
        draw_board(screen, CELL_SIZE)
        draw_discs(screen, board, CELL_SIZE)

    font = pygame.font.SysFont(None, 48)
    message = font.render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(message, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# 勝者の表示（パス表示なし）
def show_winner(screen, board, WIDTH, HEIGHT, CELL_SIZE):
    black_count = sum(row.count((0, 0, 0)) for row in board)
    white_count = sum(row.count((255, 255, 255)) for row in board)
    if black_count > white_count:
        text = "You win!"
    elif black_count < white_count:
        text = "You lose!"
    else:
        text = "It's a draw!"
    show_message(screen, text, WIDTH, HEIGHT, redraw_background=True, CELL_SIZE=CELL_SIZE, board=board)
