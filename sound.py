import pygame
import os

pygame.mixer.init()

# 効果音ファイルパス（拡張子は正確に）
BLACK_SOUND_PATH = "assets/sounds/place_black.wav"
WHITE_SOUND_PATH = "assets/sounds/place_white.wav"
BGM_PATH = "assets/sounds/bgm.mp3"

# 効果音の読み込み
try:
    place_black = pygame.mixer.Sound(BLACK_SOUND_PATH)
except FileNotFoundError:
    print(f"⚠️ 効果音が見つかりません: {BLACK_SOUND_PATH}")
    place_black = None

try:
    place_white = pygame.mixer.Sound(WHITE_SOUND_PATH)
except FileNotFoundError:
    print(f"⚠️ 効果音が見つかりません: {WHITE_SOUND_PATH}")
    place_white = None

# 効果音再生用関数を定義する
def play_black_sound():
    if place_black:
        place_black.play()

def play_white_sound():
    if place_white:
        place_white.play()

# BGM再生関数
def play_bgm():
    if os.path.isfile(BGM_PATH):
        pygame.mixer.music.load(BGM_PATH)
        pygame.mixer.music.play(-1)
    else:
        print(f"⚠️ BGMファイルが見つかりません: {BGM_PATH}")
