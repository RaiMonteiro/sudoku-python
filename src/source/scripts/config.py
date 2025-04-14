# Global variables
import pygame
from components.cursor import Cursor
from scripts.utils import StateManager, Timer
from scripts.stats import Statistics
from components.particles import Particles, Animate
from r_notes.releaseNotes import InputButtonToNotes, Notes

FPS = 30
WIN_WIDTH = 1200
WIN_HEIGHT = 800
CELL_SIZE = 70
DISPLAYSURF = None
FPSCLOCK = None
FONT_CFG = None

# colors
BLACK     = (  0 ,  0 ,  0  )
WHITE     = ( 255, 255, 255 )
RED       = ( 255,  0 ,  0  )
MARRON    = ( 128,  0 ,  0  )
DARKBROWN = ( 41 , 13 ,  0  )
BISQUE    = ( 255, 228, 196 )

# assets
ASSETS = [
    Animate('./assets/img/tree', delay=6),
    pygame.image.load('./assets/img/section.png'),
    pygame.image.load('./assets/img/game-board.png'),
    pygame.image.load('./assets/img/timer-box.png'),
    pygame.image.load('./assets/img/block.png'),
    pygame.image.load('./assets/img/btn-texture.png'),
    pygame.image.load('./assets/img/logo-menu.png'),
    pygame.image.load('./assets/img/logo.png')
]
SOUNDS = None

# game variables
DIFFICULTY = [["Fácil", 7, 35, 6000], ["Médio", 6, 30, 8000], ["Difícil", 5, 25, 10000]]
sudoku = {
    "solved": [[0 for _ in range(9)] for _ in range(9)],
    "maped": [[0 for _ in range(9)] for _ in range(9)],
    "static": [[0 for _ in range(9)] for _ in range(9)]
    }
subgrid_d = [1 for _ in range(9)]
errors = 0
level = None
user_name = str()
timer = Timer()
current_pts = None

# global objects
c = Cursor()
particles = Particles()
manager = StateManager()
statistics = Statistics()
releasenotes_btn = InputButtonToNotes()
releasenotes = Notes()

# utility variables
btns = None # list of buttons
blcs = None  # list of blocks
last_change = [None, None, None] # ln, col, num