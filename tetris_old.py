import random
import numpy as np
import time
from pynput import keyboard
import threading

BOARD_WIDTH = 10
BOARD_HEIGHT = 20


I_PIECE = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

J_PIECE = np.array([
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
])

L_PIECE = np.array([
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
])

O_PIECE = np.array([
    [1, 1],
    [1, 1]
])

S_PIECE = np.array([
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0]
])

T_PIECE = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0]
])

Z_PIECE = np.array([
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0]
])



PIECES = [I_PIECE, J_PIECE, L_PIECE, O_PIECE, S_PIECE, T_PIECE, Z_PIECE]
PIECES = [I_PIECE]

for piece in PIECES:
    for row in piece:
        print(row.T) 
    print("\n\n")


class TetrisBoard:
    def __init__(self, board_width=BOARD_WIDTH, board_height= BOARD_HEIGHT):
        self.board_width = board_width
        self.board_height = board_height
        self.board = np.array([np.array([0] * board_width) for _ in range(board_height)])
        self.prev_valid_move_board_state = self.board.copy()
        self.game_over = False
        self.current_col = 5
        self.current_row = 1
        self.added_rows = 0
        self.added_cols = 0
        self.current_piece = random.choice(PIECES)
        self.trimmed_piece = self._trim_piece(self.current_piece)
        self.next_piece = random.choice(PIECES)


    def generate_new_piece(self):
        self.current_piece = self.next_piece.copy()
        self.trimmed_piece = self._trim_piece(self.current_piece)
        self.next_piece = random.choice(PIECES)
        self.current_col = 5
    
    def rotate_piece(self):
        # test 4 positions - 1) basic rotation, 2) basic rotation + 1 wall kick to the right, 3) basic rotation + 1 wall kick to the left, 4) basic rotation + 2 wall kicks to the right
        # if any of the 4 positions are valid, the piece is rotated to that position
        # if none of the 4 positions are valid, the rotation fails completely
        #create a function that rotates the piece
        temp_current_piece = np.rot90(self.current_piece, -1)
        temp_trimmed_piece = self._trim_piece(temp_current_piece)
        #check if the piece is out of bounds

        #check if the piece is colliding with another piece
        temp_board = self.board.copy()
        for i in [0, 1, -2, 2, -1]:
            if self.current_col + temp_trimmed_piece.shape[1] + i > self.board_width or self.current_col + i < 0:
                continue
            else:
                if np.any((temp_board[self.current_row:self.current_row+temp_trimmed_piece.shape[0], self.current_col + i:self.current_col + i + temp_trimmed_piece.shape[1]] + temp_trimmed_piece) > 1):
                    continue
                else:
                    temp_board[self.current_row:self.current_row+temp_trimmed_piece.shape[0], self.current_col + i:self.current_col + i + temp_trimmed_piece.shape[1]] += temp_trimmed_piece
                    self.current_piece = temp_current_piece
                    self.trimmed_piece = temp_trimmed_piece
                    self.prev_valid_move_board_state = temp_board
                    self.current_col += i
                    return
        if self.current_col + self.trimmed_piece.shape[1] < self.board_width:
            self.current_col += 1

    def _trim_piece(self, piece):
        # trim the piece to remove empty rows and columns
        # find indices of first and last non-zero elements along each axis
        nonzero_rows = np.nonzero(piece.any(axis=1))[0]
        nonzero_cols = np.nonzero(piece.any(axis=0))[0]
        # slice the original array using the indices we found
        trimed_piece = piece[nonzero_rows.min():nonzero_rows.max()+1, nonzero_cols.min():nonzero_cols.max()+1]

        self.current_row += min(nonzero_rows) - self.added_rows
        self.added_rows = min(nonzero_rows)
        self.current_col += min(nonzero_cols) - self.added_cols
        self.added_cols = min(nonzero_cols)
        return trimed_piece

    def _move_piece_down(self):
        piece = self.trimmed_piece
        temp_board = self.board.copy()
        print()

        temp_board[self.current_row:self.current_row+piece.shape[0], self.current_col:self.current_col + piece.shape[1]] += piece
        # check for collision

        if np.any(temp_board[self.current_row:self.current_row+piece.shape[0], self.current_col:self.current_col + piece.shape[1]] > 1):
            self._lock_piece()
            print('lock 1')
            return True
        else:
            self.prev_valid_move_board_state = temp_board

        if self.current_row + piece.shape[0] >= self.board_height:
            self._lock_piece()
            return True
        self.current_row += 1
        self.prev_valid_move_board_state = temp_board
        return False

    def _lock_piece(self):
        print("\n\n\nHERE\n\n\n")
        temp_board = self.board.copy()
        piece = self.trimmed_piece
        if self.current_row + piece.shape[0] + 1 < self.board_height:
            if temp_board[self.current_row + piece.shape[0] + 1][self.current_col] != 1:
                return
        temp_board[self.current_row:self.current_row+piece.shape[0], self.current_col:self.current_col + piece.shape[1]] += piece
        print(temp_board, "\n\n\nHERE\n\n\n\n\n\n")
        self.board = self.prev_valid_move_board_state.copy()
        self.generate_new_piece()
        self.current_row = 1
    
    def print_board(self, board_type='current'):
        if board_type == 'current':
            board = self.board
        else:
            board = self.prev_valid_move_board_state
        for row in board:
            for cell in row:
                print(cell, end=f' ')
            print(f'row:{self.current_row} col:{self.current_col} shape:{self.trimmed_piece.shape}')
        print()

board = TetrisBoard()


def printit():
    threading.Timer(0.5, printit).start()
    board._move_piece_down()
    board.print_board(board_type='next')

printit()

def on_press(key):
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k == 'left':
        board.move_left()
    elif k == 'right':
        board.move_right()
    elif k == 'r':
        board.rotate_piece()
    elif k == 'space':
        while not board._move_piece_down():
            pass
    board.print_board(board_type='next')

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys

