import pygame, sys, random
from pygame.locals import *


from constants import *
from board import Board

class Game(object):

    def __init__(self):
        #Initialization
        self.total_shots = 0
        self.hit_shots = 0

        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 30)

        self.board = Board(BOARDHEIGHT, BOARDWIDTH)
        # self.board.add_ship(length=3, orientation=Board.HORIZONTAL, row=0, col=0)
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.total_shots = self.board.add_random_ships(2)

        # self.debug()

        while True:
            #Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP: #otherwise
                    mousex, mousey = event.pos #set mouse positions to the new position
                    #mouse_clicked = True #mouse is clicked but not on a button
                    col, row = self._get_tile_at_pixel(mousex, mousey)
                    if isinstance(col, int):
                        if self.board.click_ship(row, col):
                            self.hit_shots += 1
                    if self.board.is_game_finished():
                        self.end_game()
                        break

            if not self.board.is_game_finished():
                self._refresh_view()

    def _refresh_view(self):
        self.screen.fill(gray)
        self.draw()
        self.draw_shots()
        pygame.display.update()

    def debug(self):
        print("Bord before adding ship on [0][0]: ")
        for row in self.board.grid:
            print(row)
        self.board.add_ship(length=3, orientation=Board.HORIZONTAL, row=0, col=0)
        print("Board after adding ship")
        for row in self.board.grid:
            print(row)

    def draw_shots(self):
        self.shots = self.myfont.render("You hit "+(str(self.hit_shots)+" from "+str(self.total_shots))+" ships", 1, (255,255,255))
        self.screen.blit(self.shots, (10,10))

    def _paint_tile(self, row, col, color):
        left, top = self._left_top_coords_tile(row, col)
        pygame.draw.rect(self.screen, color, (left, top, tile_size, tile_size))

    def draw(self):
        for row in xrange(self.board.height):
            for col in xrange(self.board.width):
                color = self.board.get_color(row, col)
                self._paint_tile(col, row, color)

        #Draw horizontal lines
        for x in xrange(0, (BOARDWIDTH + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x, margin_y + x), (margin_x + tile_size * BOARDWIDTH, margin_y + x))
        #     pygame.draw.line(self.screen, darkgrey, (x + margin_x + MARKERSIZE,
        #         margin_y + MARKERSIZE), (x + margin_x + MARKERSIZE,
        #         window_height - margin_y))
        #Draw vertical lines
        for y in xrange(0, (BOARDHEIGHT + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + y, margin_y), (margin_x + y, margin_y + tile_size * BOARDHEIGHT))
            # pygame.draw.line(self.screen, darkgrey, (margin_x,margin_y), (margin_x*tile_size*BOARDHEIGHT+y, margin_y))

            # pygame.draw.line(self.screen, darkgrey, (margin_x + MARKERSIZE, y +
            #     margin_y + MARKERSIZE), (window_width - (display_width + MARKERSIZE *
            #     2), y + margin_y + MARKERSIZE))

    def end_game(self):
        self.screen.fill(gray)
        self.label = self.myfont.render("You won!", 1, (255,255,255))
        self.screen.blit(self.label, ((window_width/2)-80, window_height/2))
        pygame.display.update()
        print("Koniec gry")

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

    def _left_top_coords_tile(self, row, col):
        """
        Function calculates and returns the pixel of the tile in the top left corner

        row -> int; x position of tile
        col -> int; y position of tile
        returns tuple (int, int) which indicates top-left pixel coordinates of tile
        """
        left = row * tile_size + margin_x
        # left = row * tile_size + margin_x + MARKERSIZE
        top = col * tile_size + margin_y
        # top = tiley * tile_size + margin_y + MARKERSIZE
        return (left, top)
