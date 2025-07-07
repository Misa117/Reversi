import pygame
import sys
import json
import os
from game import board, ROWS, COLS, init_board, place_disc, get_legal_moves
from graphics import draw_board, draw_discs, show_message, show_winner
from player import choose_ai_move
import sound  # サウンドモジュール

pygame.init()
SCORE_FILE = 'scores.json'

# BGMを再生
sound.play_bgm()

def save_turn_score(black_count, white_count):
    data = {"black": black_count, "white": white_count}
    with open(SCORE_FILE, 'w') as f:
        json.dump(data, f)

def show_turn_score(screen, black, white, WIDTH, HEIGHT):
    font = pygame.font.SysFont(None, 28)
    text = f"Black: {black}  White: {white}"
    score_surf = font.render(text, True, (255, 255, 255))
    screen.blit(score_surf, (WIDTH - 200, HEIGHT - 30))

# ウィンドウのサイズなど設定
WIDTH, HEIGHT = 640, 640
MARGIN = 40
BOARD_SIZE = WIDTH - 2 * MARGIN
CELL_SIZE = BOARD_SIZE // COLS

# 色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("オセロ")

current_player = BLACK
init_board()

def main():
    global current_player
    clock = pygame.time.Clock()

    while True:
        legal_moves = get_legal_moves(current_player)

        if current_player == BLACK:
            show_message(screen, "player", WIDTH, HEIGHT)
        else:
            show_message(screen, "computer", WIDTH, HEIGHT)

        if not legal_moves:
            current_player = WHITE if current_player == BLACK else BLACK
            if not get_legal_moves(current_player):
                show_winner(screen, board, WIDTH, HEIGHT, CELL_SIZE)
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
            show_message(screen, "pass!", WIDTH, HEIGHT)
            continue

        move_made = False
        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and current_player == BLACK:
                    x, y = pygame.mouse.get_pos()
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN) // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if (row, col) in legal_moves:
                            place_disc(row, col, BLACK)
                            sound.play_black_sound()
                            current_player = WHITE
                            move_made = True

            if current_player == WHITE and not move_made:
                pygame.time.wait(500)
                move = choose_ai_move(WHITE)
                if move:
                    place_disc(move[0], move[1], WHITE)
                    sound.play_white_sound()
                current_player = BLACK
                move_made = True

            draw_board(screen, CELL_SIZE, MARGIN)
            draw_discs(screen, board, CELL_SIZE, MARGIN)

            black_count = sum(row.count(BLACK) for row in board)
            white_count = sum(row.count(WHITE) for row in board)
            save_turn_score(black_count, white_count)
            show_turn_score(screen, black_count, white_count, WIDTH, HEIGHT)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
