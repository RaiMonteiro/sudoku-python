import pygame
import random
import math
from pathlib import Path
import config as cfg

class Particles:
    def __init__(self):
        self.particles = []
        self.probability = 0.05 # probability of a leaf being spawn

    def add(self, obj: object):
        self.particles.append(obj)

    def kill(self, objPos: tuple):
        self.particles = [ob for ob in self.particles if not (ob.pos[0] == objPos[0] and ob.pos[1] == objPos[1])] # remove the object from the list of particles

    def setRandomPos(self, rect: tuple):
        rect_x, rect_y, rect_w, rect_h = rect
        pos = [random.randint(rect_x, rect_x + rect_w), random.randint(rect_y, rect_y + rect_h)]
        return pos

    def drawAll(self):
        for obj in self.particles:
            obj.draw()

    def removeAll(self):
        for particle in self.particles: del particle
        self.particles.clear()

    def leaFall(self): # leaf function
        leaf_spawners = [(470, 0, 200, 50), (750, 10, 400, 150), (250, 200, 150, 100), (400, 70, 300, 100), (380, 320, 120, 120)]
        if self.probability > random.random() * 100:
            cfg.particles.add(Leaf(cfg.particles.setRandomPos(leaf_spawners[random.randint(0, 4)])))
            self.probability = 0.05
        else: self.probability += 0.05

class Animate:
    def __init__(self, path: str, frame: int = 0, delay: int = 0):
        self.path = path
        self.current_frame = frame
        self.loop = None
        self.delay = delay
        self.f_counter = 0
        self.asset_files = [item.name for item in Path(path).iterdir()] # stores all the asset's frame from the corresponding files
        self.assets = [pygame.image.load(f'{self.path}/{f}') for f in self.asset_files] # loading all assets

    def render(self, pos: tuple = (0, 0), loop: bool = False):
        self.loop = loop
        if self.loop:
            self.f_counter += 1
            if self.f_counter == self.delay:
                self.f_counter = 0
                if self.current_frame + 1 <= len(self.assets) - 1: self.current_frame += 1
                else: self.current_frame = 0

        cfg.DISPLAYSURF.blit(self.assets[self.current_frame], pos)

class Leaf:
    def __init__(self, pos: list):
        self.pos = pos
        self.img = pygame.image.load('./assets/img/leaf.png').convert_alpha()
        self.opacity = 0
        self.swing = random.uniform(0, math.pi * 2) # starting swing point
        self.amplitude = random.randint(1, 3) # defines how much the leaf will balancing

        ## iniciar a animação

    def update(self):
        # movement
        self.swing += 0.1 # smooth transition
        self.pos[0] -= math.sin(self.swing) + self.amplitude
        self.pos[1] += 2
        # opacity
        if self.opacity != 255: self.opacity += 5
        # delete object
        if self.pos[0] + self.img.get_width() < 0 or self.pos[1] > cfg.WIN_HEIGHT: cfg.particles.kill(self.pos)

    def draw(self):
        self.update()
        self.img.set_alpha(self.opacity)
        cfg.DISPLAYSURF.blit(self.img, self.pos)
        # pygame.draw.rect(cfg.DISPLAYSURF, cfg.BLACK, (self.pos[0], self.pos[1], 2, 2), 0, 0)

        ## chamar a animação

    # ## retirar quando acabar toda a edição das folhas
    # def __del__(self):
    #     print("Deletou com sucesso")