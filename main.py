import pygame
from pygame.locals import *
from pygame import mixer
import pygame.midi as midi


class GameBoard:
    def __init__(self):
        # 12 x 12 board
        self._board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # border
                       [-1, 25, -1, -1, 20, -1, -1, 19, 20, 21, 20, -1],  # 1
                       [-1, 24, 23, -1, 19, 18, 17, 18, -1, -1, 19, -1],  # 2
                       [-1, -1, 22, 21, 20, -1, 16, -1, 16, 17, 18, -1],  # 3
                       [-1, 22, -1, 22, 21, -1, 15, 14, 15, 16, -1, -1],  # 4
                       [-1, 21, 20, -1, 22, 23, -1, 13, 14, -1, -1, -1],  # 5
                       [-1, 20, 19, 20, 21, -1, 11, 12, -1, -1, -1, -1],  # 6
                       [-1, -1, 18, -1, -1, -1, 10, -1, 4, 3, 2, -1],  # 7
                       [-1, 18, 17, -1, 11, 10, 9, -1, 5, -1, 1, 0],  # 8
                       [-1, 17, 16, -1, 12, -1, 8, 7, 6, -1, -1, -1],  # 9
                       [-1, -1, 15, 14, 13, -1, 9, -1, 7, 8, 9, -1],  # 10
                       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]  # border
        self._player_pos = (1, 10)
        self._square_size = 10
        self._player_img = pygame.Rect(self._player_pos[1] * self._square_size,
                                       self._player_pos[0] * self._square_size, self._square_size, self._square_size)
        # midi stuff
        midi.init()
        self._port = midi.get_default_output_id()
        self._out = midi.Output(self._port, 0)
        self._instrument = 0
        self._out.set_instrument(self._instrument)

    def get_player_pos(self):
        return self._player_pos

    def set_player_pos(self, row, col):
        self._player_pos = self._player_pos[0] + row, self._player_pos[1] + col
        self._player_img.topleft = (self._player_pos[1] * self._square_size, self._player_pos[0] * self._square_size)

    def move(self, row, col):
        """x and y should be +/- 1"""
        player_row, player_col = self.get_player_pos()
        if self._board[player_row + row][player_col + col] >= 0:
            self.set_player_pos(row, col)
        else:
            self._out.note_on(50, 90)
        if self._board[self._player_pos[0]][self._player_pos[1]] == 0:
            # activate win state
            pass

    def sonar(self):
        pitch = self._board[self._player_pos[0]][self._player_pos[1]]
        self._out.note_on(127 - (pitch * 5), 127)

    def draw_board(self, draw_screen):
        for row in range(12):
            for col in range(12):
                if self._board[row][col] == -1:
                    pygame.draw.rect(draw_screen, (255, 255, 255),
                                     pygame.Rect(col * self._square_size, row * self._square_size,
                                                 self._square_size, self._square_size))
        pygame.draw.rect(draw_screen, (0, 255, 0), self._player_img)


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Maze Game")

    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # test - rectangle
    gameboard = GameBoard()



    # event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    gameboard.move(-1, 0)
                if event.key == K_DOWN:
                    gameboard.move(1, 0)
                if event.key == K_LEFT:
                    gameboard.move(0, -1)
                if event.key == K_RIGHT:
                    gameboard.move(0, 1)
                if event.key == K_SPACE:
                    gameboard.sonar()
            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN or event.key == K_RIGHT or event.key == K_LEFT:
                    pass
        #screen.blit(background, (0, 0))
        #gameboard.draw_board(screen)
        pygame.display.flip()




if __name__ == "__main__":
    main()
