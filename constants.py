import pygame
tile_size = 40 #Size of the squares in each grid(tile)
tile = pygame.Rect(10,10,50,50)
BOARDWIDTH = 8
BOARDHEIGHT = 8
window_width = 1000 #WINDOWWIDTH
window_height = 600 #WINDOWHEIGHT
display_width = 200 #Width of game board
# MARKERSIZE = 0
margin_x = 50
# margin_x = int((window_width - (BOARDWIDTH * tile_size) - display_width - MARKERSIZE) / 2) #x-position of the top left corner of board
margin_y = 100
# margin_y = int((window_height - (BOARDHEIGHT * tile_size) - MARKERSIZE) / 2) #y-position of the top left corner of board
TILESIZE = 40

#Kolory
gray = (60,  60,  60)
black = (0,0,0)
darkgrey =( 40,  40,  40)
green   = (  0, 204,   0)
yellow = (255, 255,   0)
white   = (255, 255, 255)
