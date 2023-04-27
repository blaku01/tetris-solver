import numpy as np
import pygame


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



PIECES = np.array([I_PIECE, J_PIECE, L_PIECE, O_PIECE, S_PIECE, T_PIECE, Z_PIECE])


class TetrisGame:
    def __init__(self, width=10, height=20) -> None:
        self.board_width = width
        self.board_height = height
        self.board = None # array of zeros with border of 3 ones on each side
        self.clear_board()
        self.possible_pieces = PIECES
        self.piece_x = 8
        self.piece_y = 3
        self.piece_rotation = 0
        self.piece = np.random.choice(self.possible_pieces)
        self.next_piece = np.random.choice(self.possible_pieces)
        self.score = 0

    def clear_board(self):
        board = np.zeros((self.board_height + 6, self.board_width + 6))

        # Fill the border with ones
        board[:3, :] = 1  # Top rows
        board[-3:, :] = 1  # Bottom rows
        board[:, :3] = 1  # Left columns
        board[:, -3:] = 1  # Right columns

        self.board = board

    def clear_row_if_possible(self):
        # naive implementation - could use slice of an array, which will be faster and more readable.
        for row in range(3, self.board_height+3):
            if np.all(self.board[row, :] == 1):
                self.board[4:row+4, :] = self.board[3:row+3, :]
                self.board[3, 3:-3] = 0
                self.score += 1

    def set_random_piece(self):
        self.piece = self.next_piece
        self.next_piece = np.random.choice(self.possible_pieces)
        self.piece_rotation = 0
        self.piece_x = 8
        self.piece_y = 3

    def check_is_pos_is_valid(self, pos, piece=None):
        if piece is None:
            piece = self.piece
        if not np.any((self.board[pos[0]:pos[0]+piece.shape[0], pos[1]:pos[1]+piece.shape[1]] + piece) > 1):
            return True
        return False

    def move_piece_left(self):
        if self.check_is_pos_is_valid((self.piece_y, self.piece_x-1)):
            self.piece_x -= 1

    def move_piece_right(self):
        if self.check_is_pos_is_valid((self.piece_y, self.piece_x+1)):
            self.piece_x += 1

    def move_piece_down(self):
        # returns True if piece is placed on the board
        if self.check_is_pos_is_valid((self.piece_y+1, self.piece_x)):
            self.piece_y += 1
            return False
        else:
            self.board[self.piece_y:self.piece_y+self.piece.shape[0], self.piece_x:self.piece_x+self.piece.shape[1]] += self.piece
            self.clear_row_if_possible()
            self.set_random_piece()
            return True

    def rotate_piece(self):
        piece = np.rot90(self.piece, -1)
        if self.check_is_pos_is_valid((self.piece_y, self.piece_x), piece):
            self.piece = piece
        elif self.check_is_pos_is_valid((self.piece_y, self.piece_x+1), piece):
            self.piece = piece
            self.piece_x += 1
        elif self.check_is_pos_is_valid((self.piece_y, self.piece_x-1), piece):
            self.piece = piece
            self.piece_x -= 1
        else:
            piece = np.rot90(self.piece, 1)
            if self.check_is_pos_is_valid((self.piece_y, self.piece_x), piece):
                self.piece = piece
            elif self.check_is_pos_is_valid((self.piece_y, self.piece_x+1), piece):
                self.piece = piece
                self.piece_x += 1
            elif self.check_is_pos_is_valid((self.piece_y, self.piece_x-1), piece):
                self.piece = piece
                self.piece_x -= 1

    def run(self):
        screen = pygame.display.set_mode(((self.board_width+6)*20, (self.board_height+6)*20))
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()
        running = True
        tick = 0
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if keys[pygame.K_UP]:
                        self.rotate_piece()
                    if keys[pygame.K_SPACE]:
                        while not self.move_piece_down():
                            pass
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.move_piece_left()
            if keys[pygame.K_RIGHT]:
                self.move_piece_right()
            if keys[pygame.K_DOWN]:
                self.move_piece_down()


                
            screen.fill((0, 0, 0))
            # Draw board
            for row in range(self.board_height+6):
                for col in range(self.board_width+6):
                    if self.board[row, col] == 1:
                        pygame.draw.rect(screen, (255, 255, 255), (col*20, row*20, 20, 20))
            # Draw piece
            for row in range(self.piece.shape[0]):
                for col in range(self.piece.shape[1]):
                    if self.piece[row, col] == 1:
                        pygame.draw.rect(screen, (255, 255, 255), ((col+self.piece_x)*20, (row+self.piece_y)*20, 20, 20))
            
            pygame.display.flip()
            clock.tick(30)
            tick += 1
            if tick % 100 == 0:
                self.move_piece_down()

if __name__ == "__main__":
    game = TetrisGame()
    print('], ['.join(map(str,[','.join(map(str, [int(i) for i in item])) for item in game.board])))
    game.run()
