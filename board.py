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
        # nodes = [[Node() for j in range(cols)] for i in range(rows)]
        self.grid = [ [Field() for j in range(cols)] for i in range(rows) ]
        self.total_ships_length = 0
        self.hit_shots = 0
        self.last_shot = False
        self.last_shot_row = 0
        self.last_shot_col = 0

        #New ship values
        self.new_ship_col = []
        self.new_ship_row = []
        self.new_ship_length = 0
        self.new_ship_orientation = Board.HORIZONTAL

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

    def add_ships_manual(self, number_of_human_ships, row, col):
        # orientation = [Board.HORIZONTAL, Board.VERTICAL]
        # direction = random.choice(orientation)
        # self.add_ship(number_of_human_ships, direction, row, col)
        print "Wspolrzedne [{}][{}], statek dlugosci {}/{}".format(col, row, self.new_ship_length , number_of_human_ships)
        if self.new_ship_length == number_of_human_ships:
            self.add_ship(self.new_ship_length, self.new_ship_orientation, self.new_ship_row[0], self.new_ship_col[0])
            print "new_ship_length {} == {} number_of_human_ships".format(self.new_ship_length, number_of_human_ships)

            #Reset values
            print "Resetuje wartosci statku {}".format(number_of_human_ships)
            self.new_ship_col = []
            self.new_ship_row = []
            self.new_ship_length = 0
            self.new_ship_orientation = Board.HORIZONTAL

            print "Zwracam True dla statku numer {}".format(number_of_human_ships)
            return True
        else:
            if self.new_ship_length == 0:
                self.new_ship_col.append(col)
                self.new_ship_row.append(row)
                self.new_ship_length += 1
                print "nowa dlugosc statku: {}".format(self.new_ship_length)
                self.add_ships_manual(number_of_human_ships, row, col)
                return False
            elif self.new_ship_length == 1:
                print "new_ship_length = 1"
                if col != self.new_ship_col[0] and row != self.new_ship_row[0]:
                    print "Pierwszy if"
                    return False
                elif col != self.new_ship_col[0] and row == self.new_ship_row[0]:
                    print "Drugi if"
                    self.new_ship_orientation = Board.VERTICAL
                    self.new_ship_col.append(col)
                    self.new_ship_row.append(row)
                    self.new_ship_length += 1
                    self.add_ships_manual(number_of_human_ships, row, col)
                    return False
                elif col == self.new_ship_col[0] and row != self.new_ship_row[0]:
                    print "Trzeci if"
                    self.new_ship_orientation = Board.HORIZONTAL
                    self.new_ship_col.append(col)
                    self.new_ship_row.append(row)
                    self.new_ship_length += 1
                    self.add_ships_manual(number_of_human_ships, row, col)
                    return False
            elif self.new_ship_length >= 2:
                if self.orientation == Board.VERTICAL:
                    if col != self.new_ship_col[0]:
                        return False
                    else:
                        self.new_ship_col.append(col)
                        self.new_ship_row.append(row)
                        self.new_ship_length += 1
                        self.add_ships_manual(number_of_human_ships, row, col)
                        return False
                elif self.orientation == Board.HORIZONTAL:
                    if row != self.new_ship_row[0]:
                        return False
                    else:
                        self.new_ship_col.append(col)
                        self.new_ship_row.append(row)
                        self.new_ship_length += 1
                        self.add_ships_manual(number_of_human_ships, row, col)
                        return False

    def are_fields_empty(self, length, orientation, row, col):
        if orientation == Board.HORIZONTAL and col+length<=BOARDWIDTH:
            for current_column in range(col+length):
                if self.grid[row][current_column].ship or self.grid[row+1][current_column].ship or self.grid[row-1][current_column].ship:
                    return False
        elif orientation == Board.VERTICAL and row+length<=BOARDHEIGHT:
            for current_row in range(row, row+length):
                if self.grid[current_row][col].ship or self.grid[current_row][col-1].ship or self.grid[current_row][col+1].ship:
                    return False
        return True

    def get_color(self, row, col):
        field = self.grid[row][col]
        if field.ship == True:
            return yellow if field.reveal else white

        if field.reveal == True:
            return gray
        return green

    def click_ship(self, row, col):
        field = self.grid[row][col]
        if field.reveal:
            return False
        else:
            field.reveal = True
            # self.last_shot = False
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
            col = BOARDWIDTH
        if row != self.last_shot_row:
            col=self.last_shot_col
        else:
            row = self.last_shot_row
        try:
            if not self.click_ship(row, col):
                self.near_shot()
        except RuntimeError as re:
            if re.args[0] != 'maximum recursion depth exceeded while calling a Python object':
                # different type of runtime error
                raise
            self.last_shot = False
            self.random_shot()

    def random_shot(self):
        row = random.randint(0,BOARDHEIGHT-1)
        col = random.randint(0, BOARDWIDTH-1)
        if not self.click_ship(row, col):
            self.random_shot()
