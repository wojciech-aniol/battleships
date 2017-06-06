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
        self.computer_grid = []
        # nodes = [[Node() for j in range(cols)] for i in range(rows)]
        self.grid = [ [Field() for j in range(cols)] for i in range(rows) ]
        self.computer_grid = [ [Field() for j in range(cols)] for i in range(rows) ]

    def is_game_finished(self):
        flat = sum(self.grid, [])
        revealed_field_tester = lambda field: field.ship and (not field.reveal)
        return len(filter(revealed_field_tester, flat)) == 0

    def are_fields_empty(self, length, orientation, row, col):
        if orientation == Board.HORIZONTAL and col+length<=BOARDWIDTH:
            for current_column in range(col+length):
                if self.grid[row][current_column].ship == True:
                    return False
        elif orientation == Board.VERTICAL and row+length<=BOARDHEIGHT:
            for current_row in range(row, row+length):
                if self.grid[current_row][col].ship == True:
                    return False
        return True

    def add_random_ship(self, length):
        orientation = [Board.HORIZONTAL, Board.VERTICAL]
        row = random.randint(0,BOARDHEIGHT-length)
        col = random.randint(0,BOARDWIDTH-length)
        direction = random.choice(orientation)
        try:
            self.add_ship(length=length, orientation=random.choice(orientation), row=row, col=col)
        except exceptions.FieldTakenException as e:
            self.add_random_ship(length)

    def add_random_ships(self, num):
        total_length = 0
        for i in range(1, num+1):
            self.add_random_ship(i)
            total_length += i
        return total_length

    def add_ship(self, length, orientation, row, col):
        # FIXME! sprawdz czy nie istnieje tu inny statek albo jestes poza plansza FIXME!
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

    def get_color(self, row, col):
        field = self.grid[row][col]
        if field.ship == True:
            return yellow if field.reveal else white

        if field.reveal == True:
            return gray
        return green

    def click_ship(self, row, col):
        # ship = self.grid[row][col]
        # is_ship_present = ship in not True
        # if is_ship_present:
        #     # print "setting reveal at {} {}".format(row, col)
        #     ship.reveal = True
        # return is_ship_present
        #-------
        field = self.grid[row][col]
        if not field.reveal:
            field.reveal = True
            if field.ship:
                return True
        if field.ship and field.reveal:
            return False


        # if field.ship == True:
            # field.reveal = True
