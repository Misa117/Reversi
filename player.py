import random
from game import get_legal_moves

def choose_ai_move(color):
    legal = get_legal_moves(color)
    corners = [(0,0), (0,7), (7,0), (7,7)]
    for move in corners:
        if move in legal:
            return move
    return random.choice(legal) if legal else None
