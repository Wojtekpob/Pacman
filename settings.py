import pygame


# GAME SETTINGS ##
SCREEN_WIDTH = 560
TOP_EMPTY_SPACE = BOT_EMPTY_SPACE = 60
SCREEN_HEIGHT = 720
MAZE_WIDTH = 560
MAZE_HEIGHT = 620
FPS = 60
WALL_SIDE_LENGHT = 20
CELL_LENGHT = 20
PAUSE_RECT_SIDE = 500
PACMAN_ICON = 'photos/pacman.png'


# PLAYER SETTINGS ##
PLAYERS_WIDTH = 20
PLAYERS_HEIGHT = 20
PLAYERS_STARTING_POSITION = 280, 520
PLAYERS_SPEED = 2
PLAYER_PHOTO = 'photos/pacman_player.png'

# CONSUMABLES SETTINGS ##
COIN_RADIOUS = 2
COIN_VALUE = 10
POWERUP_VALUE = 50

# COLORS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (235, 235, 63)
RED = (255, 0, 0)
PINK = (252, 0, 215)
ORANGE = (252, 186, 3)
TURQUOISE = (24, 199, 187)
BLUE = (0, 250, 212)
GREEN = (52, 235, 61)
DARK_GREEN = (20, 112, 39)


# GHOSTS ##
RED_GHOST_STARTING_POSITION = (280, 280)
BLUE_GHOST_STARTING_POSITION = 340, 280
ORANGE_GHOST_STARTING_POSITION = 240, 280
PINK_GHOST_STARTING_POSITION = 200, 280
GHOST_WIDTH = 20
GHOST_HEIGHT = 20
GHOST_RADIOUS = 10


# EVENTS ##
frightened_mode = pygame.USEREVENT
normal_mode = pygame.USEREVENT + 1
