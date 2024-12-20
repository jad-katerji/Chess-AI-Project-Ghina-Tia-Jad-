import pygame


import pygame


class GUI:
    def __init__(self):
        """Initialize the Game GUI."""
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 600, 600
        self.SQUARE_SIZE = self.WIDTH // 8
        self.WHITE = (255, 255, 255)
        self.BROWN = (139, 69, 19)

        # Load chess piece images
        self.PIECE_IMAGES = {}
        for piece in ['wp', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bp', 'bN', 'bB', 'bR', 'bQ', 'bK']:
            self.PIECE_IMAGES[piece] = pygame.image.load(f"assets/{piece}.png")

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess UI")

    def draw_board(self):
        """Draw the chessboard grid."""
        colors = [self.WHITE, self.BROWN]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE),
                )

    def draw_pieces(self, board):
        """Draw chess pieces based on the board state."""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != "--":
                    piece_image = self.PIECE_IMAGES[piece]
                    piece_image = pygame.transform.scale(piece_image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                    self.screen.blit(piece_image, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

    def Draw(self, board):
        """Draw the board and pieces."""
        self.screen.fill(self.WHITE)  # Clear the screen
        self.draw_board()  # Draw the grid
        self.draw_pieces(board)  # Draw the pieces
        pygame.display.flip()  # Update the display
