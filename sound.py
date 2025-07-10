import pygame
import os

pygame.mixer.init()

# 効果音読み込み用の共通関数
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except FileNotFoundError:
        print(f"⚠️ 効果音が見つかりません: {path}")
        return None

# 各種効果音の読み込み
place_black = load_sound("assets/sounds/place_black.wav")
place_white = load_sound("assets/sounds/place_white.wav")
flip_sound   = load_sound("assets/sounds/flip.wav")

# BGM再生関数
def play_bgm():
    bgm_path = "assets/sounds/bgm.mp3"
    if os.path.isfile(bgm_path):
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.play(-1)
    else:
        print(f"⚠️ BGMファイルが見つかりません: {bgm_path}")

# 効果音再生関数
def play_black_sound():
    if place_black:
        place_black.play()

def play_white_sound():
    if place_white:
        place_white.play()

def play_flip_sound():
    if flip_sound:
        flip_sound.play()
