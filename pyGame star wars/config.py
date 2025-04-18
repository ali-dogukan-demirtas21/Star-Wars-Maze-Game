import pygame


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "Star Wars"
FPS = 60


PYGAME_DISPLAY_FLAGS = 0  
FONT_NAME = "Arial"
FONT_SIZE_SMALL = 18
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
BUTTON_INACTIVE_COLOR = (150, 150, 150)
BUTTON_ACTIVE_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WALL_COLOR = (0, 0, 0)  
PATH_COLOR = (192, 192, 192)  
PLAYER_COLOR = YELLOW
ENEMY_COLOR = RED
GOAL_COLOR = GREEN


PYGAME_DISPLAY_FLAGS = pygame.FULLSCREEN  


CELL_SIZE = 80  
WALL = 0  
PATH = 1  
GRID_LINE_COLOR = (50, 50, 50)  
GRID_LINE_WIDTH = 1  


PLAYER_START_POS = (6, 5)  
PLAYER_SPEED = 5  
ENEMY_SPEED = 4   
KYLO_REN_SPEED = 8  


DOORS = {
    "A": (0, 5),    
    "B": (4, 0),    
    "C": (12, 0),   
    "D": (13, 5),   
    "E": (4, 10),   
}


GOAL_POS = (13, 9)  




MOVEMENT_KEYS = {
    "UP": [pygame.K_UP, pygame.K_w],
    "DOWN": [pygame.K_DOWN, pygame.K_s],
    "LEFT": [pygame.K_LEFT, pygame.K_a],
    "RIGHT": [pygame.K_RIGHT, pygame.K_d]
}


MUSIC_VOLUME = 0.5
EFFECT_VOLUME = 0.7
CAPTURE_SOUND = "capture.wav"
VICTORY_SOUND = "victory.wav"
GAME_OVER_SOUND = "game_over.wav"
BACKGROUND_MUSIC = "background.wav"


ANIMATION_COOLDOWN = 100  
SPRITE_SCALE = 1.5  

MAPS_DIRECTORY = "maps/"
DEFAULT_MAP = "Star wars harita.txt"
ASSETS_DIRECTORY = "assets/"
IMAGES_DIRECTORY = ASSETS_DIRECTORY + "images/"
SOUNDS_DIRECTORY = ASSETS_DIRECTORY + "sounds/"


CHARACTER_IMAGES = {
    "Luke Skywalker": "luke.png",
    "Master Yoda": "yoda.png",
    "Darth Vader": "vader.png",
    "Kylo Ren": "kylo.png",
    "Stormtrooper": "stormtrooper.png",
    "Trophy": "trophy.png"
}


HEART_IMAGES = {
    "full": "can1.png",    
    "half": "can05.png",   
    "empty": "can0.png"    
}




PATHFINDING_DELAY = 0.1  
VISUALIZE_PATHFINDING = True  