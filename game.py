import pygame, sys, random
from pygame.locals import *


from constants import *
from board import Board

class Game(object):

    HUMAN = True
    COMPUTER = False

    def __init__(self):
        #Initialization
        self.hit_shots = 0
        self.player = self.HUMAN
        self.number_of_ships = 2

        self.is_human_ships_added = False
        self.number_of_human_ships = 1


        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 30)

        self.board = Board(BOARDHEIGHT, BOARDWIDTH)
        self.comp_board = Board(BOARDHEIGHT, BOARDWIDTH)
        # self.board.add_ship(length=3, orientation=Board.HORIZONTAL, row=0, col=0)
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.board.add_random_ships(self.number_of_ships) #Add computer ship on human board
        # self.comp_board.add_random_ships(5) #Add player ship on computer board
        # self.board.add_ships_manual(5)

        while True:
            #Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP: #otherwise
                    mousex, mousey = event.pos #set mouse positions to the new position
                    col, row = self._get_tile_at_pixel(self.is_human_ships_added, mousex, mousey)
                    if self.player and self.is_human_ships_added:
                        if isinstance(col, int):
                            if self.board.click_ship(row, col):
                                self.player = Game.COMPUTER
                                self.computer_turn()
                        if self.board.is_game_finished():
                            self.end_game()
                            break
                        elif self.comp_board.is_game_finished():
                            self.end_game()
                            break
                    elif self.is_human_ships_added == False:
                        if isinstance(col, int):
                            if self.comp_board.add_ships_manual(self.number_of_human_ships, row, col) == True:
                                print "Zwrocil True, zwiekszam dlugosc statku."
                                self.number_of_human_ships += 1
                                print "Aktualnie number_of_human_ships {} / {} number_of_ships".format(self.number_of_human_ships, self.number_of_ships)
                            if self.number_of_human_ships == self.number_of_ships+1:
                                self.is_human_ships_added = True
            if self.is_human_ships_added:
                self._refresh_view()
            else:
                self.start_game()
            # if not self.is_human_ships_added:
            #     self.start_game()
            # if not self.board.is_game_finished() and not self.comp_board.is_game_finished():
            #     self._refresh_view()

    def _refresh_view(self):
        self.screen.fill(gray)
        self.draw()
        self.draw_shots()
        pygame.display.update()

    def start_game(self):
        self.screen.fill(gray)
        self.draw_empty_board()
        pygame.display.update()

    def computer_turn(self):
        if self.comp_board.last_shot:
            self.comp_board.near_shot()
        else:
            self.comp_board.random_shot()
        self.player = Game.HUMAN

    def draw_shots(self):
        self.shots = self.myfont.render("You hit "+(str(self.board.hit_shots)+" from "+str(self.board.total_ships_length))+" piece of ship", 1, (255,255,255))
        self.screen.blit(self.shots, (10,10))

    def _paint_tile(self, player, row, col, color):
        # if player == "human":
        left, top = self._left_top_coords_tile(player, row, col)
        pygame.draw.rect(self.screen, color, (left, top, tile_size, tile_size))
        # elif player=="computer":
        #     left = row * tile_size + margin_x + BOARDWIDTH*tile_size + 100
        #     top = col * tile_size + margin_y
        #     pygame.draw.rect(self.screen, color, (left, top, tile_size, tile_size))
    def draw(self):
        for row in xrange(self.board.height):
            for col in xrange(self.board.width):
                color = self.board.get_color(row, col)
                self._paint_tile("human", col, row, color)

        for row in xrange(self.comp_board.height):
            for col in xrange(self.comp_board.width):
                color = self.comp_board.get_color(row, col)
                self._paint_tile("computer", col, row, color)

        #Drawing lines
        board_width = BOARDWIDTH*tile_size
        board_height = BOARDHEIGHT*tile_size
        #Draw HUMAN horizontal lines
        for x in xrange(0, (BOARDWIDTH + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x, margin_y + x), (margin_x + board_width, margin_y + x))

        #Draw COMPUTER horizontal lines
        for x in xrange(0, (BOARDWIDTH + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + board_width + 100, margin_y + x), (margin_x + 2 * board_width + 100, margin_y + x))

        #Draw HUMAN vertical lines
        for y in xrange(0, (BOARDHEIGHT + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + y, margin_y), (margin_x + y, margin_y + board_height))

        #Draw COMPUTER vertical lines
        for y in xrange(0, (BOARDHEIGHT + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + y + board_height + 100, margin_y), (margin_x + y + board_height + 100, margin_y + board_height))

    def draw_empty_board(self):
        for row in xrange(self.comp_board.height):
            for col in xrange(self.comp_board.width):
                color = self.comp_board.get_color(row, col)
                self._paint_tile("computer", col, row, color)
        #Drawing lines
        board_width = BOARDWIDTH*tile_size
        board_height = BOARDHEIGHT*tile_size
        #Draw COMPUTER horizontal lines
        for x in xrange(0, (BOARDWIDTH + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + board_width + 100, margin_y + x), (margin_x + 2 * board_width + 100, margin_y + x))

        #Draw COMPUTER vertical lines
        for y in xrange(0, (BOARDHEIGHT + 1) * tile_size, tile_size):
            pygame.draw.line(self.screen, darkgrey, (margin_x + y + board_height + 100, margin_y), (margin_x + y + board_height + 100, margin_y + board_height))


    def end_game(self):
        self.screen.fill(gray)
        self.label = self.myfont.render("Game end!", 1, (255,255,255))
        if self.board.is_game_finished():
            self.label = self.myfont.render("You won!", 1, (255,255,255))
        elif self.comp_board.is_game_finished():
            self.label = self.myfont.render("Computer won!", 1, (255,255,255))
        self.screen.blit(self.label, ((window_width/2)-80, window_height/2))
        pygame.display.update()

    def _get_tile_at_pixel(self, is_human_ships_added, x, y):
        """
        Function finds the corresponding tile coordinates of pixel at top left, defaults to (None, None) given a coordinate.

        x -> int; x position of pixel
        y -> int; y position of pixel
        returns tuple (tilex, tiley)
        """
        if is_human_ships_added == True:
            player = "human"
            for tilex in xrange(BOARDWIDTH):
                for tiley in xrange(BOARDHEIGHT):
                    left, top = self._left_top_coords_tile(player, tilex, tiley)
                    tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                    if tile_rect.collidepoint(x, y):
                        return (tilex, tiley)
            return (None, None)
        else:
            player = "computer"
            for tilex in xrange(BOARDWIDTH):
                for tiley in xrange(BOARDHEIGHT):
                    left, top = self._left_top_coords_tile(player, tilex, tiley)
                    tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                    if tile_rect.collidepoint(x, y):
                        return (tilex, tiley)
            return (None, None)

    def _left_top_coords_tile(self, player, row, col):
        """
        Function calculates and returns the pixel of the tile in the top left corner

        row -> int; x position of tile
        col -> int; y position of tile
        returns tuple (int, int) which indicates top-left pixel coordinates of tile
        """
        if player == "human":
            left = row * tile_size + margin_x
            top = col * tile_size + margin_y
            return (left, top)
        elif player == "computer":
            left = row * tile_size + margin_x + BOARDWIDTH*tile_size + 100
            top = col * tile_size + margin_y
            return (left, top)
