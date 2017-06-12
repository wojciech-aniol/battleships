import random

from field import Field
from constants import *
from exceptions import *
from game import *

class Board(object):

    HORIZONTAL=True
    VERTICAL=False

    def __init__(self, rows, cols):
        self.width = cols
        self.height = rows
        self.grid = []

        self.grid = [ [Field() for j in range(cols)] for i in range(rows) ]
        self.total_ships_length = 0
        self.hit_shots = 0

        #Values for near_shot()
        self.last_shot = False
        self.last_shot_row = 0
        self.last_shot_col = 0

    def is_game_finished(self):
        flat = sum(self.grid, [])
        revealed_field_tester = lambda field: field.ship and (not field.reveal)
        return len(filter(revealed_field_tester, flat)) == 0

    def add_random_ships(self, num):
        for i in range(1, num+1):
            self.add_random_ship(i)

    def add_random_ship(self, length):
        orientation = [Board.HORIZONTAL, Board.VERTICAL]
        row = random.randint(0,BOARDHEIGHT-length)
        col = random.randint(0,BOARDWIDTH-length)
        direction = random.choice(orientation)
        try:
            self.add_ship(length=length, orientation=random.choice(orientation), row=row, col=col)
            self.total_ships_length += length
        except:
            self.add_random_ship(length)

    def add_ship(self, length, orientation, row, col):
        if self.are_fields_empty(length, orientation, row, col):
            if orientation == Board.HORIZONTAL:
                for current_column in range(col, col+length):
                    self.grid[row][current_column].ship = True
                return True
            elif orientation == Board.VERTICAL:
                for current_row in range(row, row+length):
                    self.grid[current_row][col].ship = True
                return True
            self.game.total_shots = self.game.total_shots + length
        else:
             raise FieldTakenException("Ship already exists on this place")

    def add_ships_manual(self, row, col):
        if self.add_ship(1, Board.HORIZONTAL, row, col):
            return True
        else:
            return False

    def are_fields_empty(self, length, orientation, row, col):
        if orientation == Board.HORIZONTAL and col+length<=BOARDWIDTH:
            for current_column in range(col, col+length-1):
                if self.grid[row][current_column].ship:
                    return False
        elif orientation == Board.VERTICAL and row+length<=BOARDHEIGHT:
            for current_row in range(row, row+length-1):
                if self.grid[current_row][col].ship:
                    return False
        return True

    def get_color(self, visible_ships, row, col):
        field = self.grid[row][col]
        if visible_ships:
            ship_color = white
        elif not visible_ships:
            ship_color = green
        if field.ship == True:
            return yellow if field.reveal else ship_color
        if field.reveal == True:
            return gray
        return green

    def click_ship(self, row, col):
        field = self.grid[row][col]
        if field.reveal:
            return False
        else:
            field.reveal = True
            if field.ship:
                self.hit_shots += 1
                self.last_shot = True
                self.last_shot_col = col
                self.last_shot_row = row
            return True

    def near_shot(self):
        row = random.randint(self.last_shot_row-1,self.last_shot_row+1)
        col = random.randint(self.last_shot_col-1, self.last_shot_col+1)
        if row >= BOARDWIDTH:
            row = BOARDWIDTH-1
        if col >= BOARDHEIGHT:
            col = BOARDHEIGHT
        try:
            if not self.click_ship(row, col):
                self.near_shot()
        except RuntimeError as re:
            if re.args[0] != 'maximum recursion depth exceeded while calling a Python object':
                raise
            self.last_shot = False
            self.random_shot()

    def random_shot(self):
        row = random.randint(0,BOARDHEIGHT-1)
        col = random.randint(0, BOARDWIDTH-1)
        if not self.click_ship(row, col):
            self.random_shot()
