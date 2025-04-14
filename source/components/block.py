import pygame
import math
import scripts.config as cfg
from scripts.utils import Centralize

class Block:
    def __init__(self, pos, num):
        self.size = 70
        self.init_pos = pos # original/initial position
        self.home_pos_x, self.home_pos_y = pos # represents where the block is currently chained
        self.pos_x, self.pos_y = pos # exact position on the screen

        self.num = num
        self.ref = [None, None] # sudoku position reference

        self.rest = True # identifies whether it is at rest and if it can perform motion calculations
        self.grabbed = False
        self.child = False
        self.delete = False # if it's able to be deleted

        # physics
        self.vel = None # the velocity depends on the distance between coordinates
        self.dx, self.dy = 0, 0

    def createChild(self): # creates a new object with the original position.
        self.child = True
        cfg.blcs.append(Block(self.init_pos, self.num))

    def calculateMovement(self):
        delta_x = self.pos_x - self.home_pos_x
        delta_y = self.pos_y - self.home_pos_y
        distance = math.sqrt(delta_x**2 + delta_y**2)
        
        # ensures the speed finishes the job
        vel_calc = round(distance / 5, 1) # a more specific calculation
        if vel_calc > 1.1: self.vel = vel_calc 
        else: self.vel = 1.0

        if distance != 0:
            self.dx = (delta_x / distance) * self.vel
            self.dy = (delta_y / distance) * self.vel
        else:
            self.dx, self.dy = 0, 0

    def referencesHandler(self, ln, col):
        if self.ref[0] != None and self.ref[1] != None:
            cfg.sudoku["maped"][self.ref[0]][self.ref[1]] = 0

        self.ref[0], self.ref[1] = ln, col
        cfg.last_change[0], cfg.last_change[1], cfg.last_change[2] = ln, col, self.num
        cfg.sudoku["maped"][ln][col] = self.num

    def checkValidArea(self):
        mouse_pos = pygame.mouse.get_pos()
        spacing_x, spacing_y = 0, 0
        for i in range(9):
            if i == 3 or i == 6: spacing_y += 10
            for o in range(9):
                if o == 3 or o == 6: spacing_x += 10

                cell_x = 50 + spacing_x + cfg.CELL_SIZE * o
                cell_y = 50 + spacing_y + cfg.CELL_SIZE * i

                if mouse_pos[0] >= cell_x and mouse_pos[0] <= cell_x + cfg.CELL_SIZE and mouse_pos[1] >= cell_y and mouse_pos[1] <= cell_y + cfg.CELL_SIZE:
                    if cfg.sudoku["maped"][i][o] == 0:
                        self.home_pos_x, self.home_pos_y = cell_x, cell_y
                        self.referencesHandler(i, o)

                        if self.child == False: self.createChild() # can only be executed once
                        return True
            spacing_x = 0
        return False

    def update(self):
        if self.grabbed:
            self.rest = False
            mouse_pos = pygame.mouse.get_pos()
            self.pos_x, self.pos_y = mouse_pos[0] - 35, mouse_pos[1] - 35
        else:
            if not self.rest: # evaluates the need to calculate the movement
                self.calculateMovement()
                if abs(self.pos_x - self.home_pos_x) > abs(self.dx) or abs(self.pos_y - self.home_pos_y) > abs(self.dy):
                    self.pos_x -= self.dx
                    self.pos_y -= self.dy
                else:
                    self.rest = True
                    self.pos_x, self.pos_y = self.home_pos_x, self.home_pos_y

    def draw(self):
        self.update()
        text_centralized = Centralize((self.pos_x, self.pos_y), (self.size - 10, self.size - 10), cfg.FONT_CFG[1].size(str(self.num)))
        cfg.DISPLAYSURF.blit(cfg.ASSETS[4], (self.pos_x, self.pos_y))
        cfg.DISPLAYSURF.blit(cfg.FONT_CFG[2].render(str(self.num), True, cfg.BISQUE), (text_centralized.xAxis(), text_centralized.yAxis()))
        
    def deleteBlock(self):
        pass

    def isHovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.pos_x and mouse_pos[0] <= self.pos_x + self.size and mouse_pos[1] >= self.pos_y and mouse_pos[1] <= self.pos_y + self.size: return True
        return False
    
    def mouseInteractions(self, event):
        if self.isHovered():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.grabbed == False and self.rest == True:
                self.grabbed = True
                cfg.c.grabbing = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.grabbed == True and self.rest == False:
                self.grabbed = False
                cfg.c.grabbing = False
                if self.checkValidArea(): cfg.SOUNDS[2].play()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and self.grabbed == False and self.rest == True:
                if self.init_pos != (self.home_pos_x, self.home_pos_y):
                    self.delete = True
                    cfg.sudoku["maped"][self.ref[0]][self.ref[1]] = 0    