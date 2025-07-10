import pygame
import sys
import json
import os
from game import board, ROWS, COLS, init_board, place_disc, get_legal_moves, get_flippable_discs
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

    # 裏返しアニメーション用変数
    flipping = False              # 裏返し中かどうか
    flip_positions = []           # 裏返す駒の位置リスト
    flip_index = 0                # 今どの駒を裏返すかのインデックス
    last_flip_time = 0            # 最後に裏返した時間（ミリ秒）
    flip_delay = 500  # 500ミリ秒（0.5秒）          # 裏返し間隔（ミリ秒）

    move_made = False             # 今ターンで置いたかどうかのフラグ

    while True:
        legal_moves = get_legal_moves(current_player)

        if current_player == BLACK:
            show_message(screen, "player", WIDTH, HEIGHT)
        else:
            show_message(screen, "computer", WIDTH, HEIGHT)

        if not legal_moves and not flipping:
            # パス処理（合法手なしかつアニメ中でない）
            current_player = WHITE if current_player == BLACK else BLACK
            if not get_legal_moves(current_player):
                show_winner(screen, board, WIDTH, HEIGHT, CELL_SIZE)
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
            show_message(screen, "pass!", WIDTH, HEIGHT)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # プレイヤーの操作は裏返し中でなければ受け付ける
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == BLACK and not flipping:
                x, y = pygame.mouse.get_pos()
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    flippable = get_flippable_discs(row, col, BLACK)
                    if flippable:
                        # 駒を置く
                        board[row][col] = BLACK
                        sound.play_black_sound()  # 黒駒の効果音
                        flip_positions = flippable
                        flip_index = 0
                        flipping = True
                        last_flip_time = pygame.time.get_ticks()
                        move_made = True

        # AIの操作（裏返し中は操作しない）
        if current_player == WHITE and not move_made and not flipping:
            pygame.time.wait(500)
            move = choose_ai_move(WHITE)
            if move:
                row, col = move
                flippable = get_flippable_discs(row, col, WHITE)
                if flippable:
                    board[row][col] = WHITE
                    sound.play_white_sound()  # 白駒の効果音
                    flip_positions = flippable
                    flip_index = 0
                    flipping = True
                    last_flip_time = pygame.time.get_ticks()
                move_made = True

        # 裏返しアニメーションの処理
        if flipping:
            now = pygame.time.get_ticks()
            if flip_index < len(flip_positions) and now - last_flip_time >= flip_delay:
                r, c = flip_positions[flip_index]
                board[r][c] = current_player  # 裏返す
                if sound.flip_sound:
                    sound.play_flip_sound()
                else:
                    print("⚠️ flip_sound がロードされていません")
                flip_index += 1
                last_flip_time = now

            if flip_index >= len(flip_positions):
                flipping = False
                move_made = False
                current_player = WHITE if current_player == BLACK else BLACK

        # 画面描画（常に行うべき！）
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
