import pygame, sys, random
from pygame.locals import *


from constants import *
from board import Board

class Game(object):

    def _left_top_coords_tile(self, tilex, tiley):
        """
        Function calculates and returns the pixel of the tile in the top left corner

        tilex -> int; x position of tile
        tiley -> int; y position of tile
        returns tuple (int, int) which indicates top-left pixel coordinates of tile
        """
        left = tilex * tile_size + margin_x + MARKERSIZE
        top = tiley * tile_size + margin_y + MARKERSIZE
        return (left, top)

    def _refresh_view(self):
        self.screen.fill(gray)
        self.draw()
        pygame.display.update()

    def debug(self):
        print("Bord before adding ship on [0][0]: ")
        for row in self.board.grid:
            print(row)
        self.board.add_ship(length=3, orientation=Board.HORIZONTAL, row=0, col=0)
        print("Board after adding ship")
        for row in self.board.grid:
            print(row)

    def end_game(self):
        pygame.quit()
        sys.exit()

    def __init__(self):
        #Initialization
        pygame.init()
        self.board = Board(BOARDHEIGHT, BOARDWIDTH)
        # self.board.add_ship(length=3, orientation=Board.HORIZONTAL, row=0, col=0)
        # self.board.add_ship(length=4, orientation=Board.VERTICAL, row=1, col=0)
        self.screen = pygame.display.set_mode((window_width, window_height))

        self.board.add_random_ships(3)


        # self.debug()

        while True:
            #Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
                elif event.type == MOUSEBUTTONUP: #otherwise
                    mousex, mousey = event.pos #set mouse positions to the new position
                    #mouse_clicked = True #mouse is clicked but not on a button
                    col, row = self._get_tile_at_pixel(mousex, mousey)
                    self.board.click_ship(row, col)
                    if self.board.is_game_finished():
                        self.end_game()



            self._refresh_view()


    def _paint_tile(self, row, col, color):
        left, top = self._left_top_coords_tile(row, col) # FIXME sprawdz czy nie trzeba miejscami zamienic row i col
        pygame.draw.rect(self.screen, color, (left, top, tile_size, tile_size))

    def draw(self):
        for row in xrange(self.board.height):
            for col in xrange(self.board.width):
                color = self.board.get_color(row, col)
                self._paint_tile(col, row, color)


        #Draw horizontal lines
        for x in xrange(0, (BOARDWIDTH + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (x + margin_x + MARKERSIZE,
                margin_y + MARKERSIZE), (x + margin_x + MARKERSIZE,
                window_height - margin_y))
        #Draw vertical lines
        for y in xrange(0, (BOARDHEIGHT + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + MARKERSIZE, y +
                margin_y + MARKERSIZE), (window_width - (display_width + MARKERSIZE *
                2), y + margin_y + MARKERSIZE))

    def _get_tile_at_pixel(self, x, y):
        """
        Function finds the corresponding tile coordinates of pixel at top left, defaults to (None, None) given a coordinate.

        x -> int; x position of pixel
        y -> int; y position of pixel
        returns tuple (tilex, tiley)
        """
        for tilex in xrange(BOARDWIDTH):
            for tiley in xrange(BOARDHEIGHT):
                left, top = self._left_top_coords_tile(tilex, tiley)
                tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if tile_rect.collidepoint(x, y):
                    return (tilex, tiley)
        return (None, None)
