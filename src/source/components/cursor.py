import pygame
import scripts.config as cfg

class Cursor:
    def __init__(self):
        self.assets = [pygame.image.load('./assets/img/cursor/cursor.png'), pygame.image.load('./assets/img/cursor/click-effect.png'), pygame.image.load('./assets/img/cursor/grabbing-effect.png')]
        self.current_state = 0
        self.clicking = False
        self.grabbing = False

    def update(self):
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()

        if self.clicking:
            self.current_state = 1
            self.pos = (mouse_pos[0] - 10, mouse_pos[1])
        else:
            self.current_state = 0
            self.pos = (mouse_pos[0] - 12, mouse_pos[1])
        
    def showCursor(self):
        self.update()
        if self.pos[0] > -12 and self.pos[0] < cfg.WIN_WIDTH - 13 and self.pos[1] > 0 and self.pos[1] <= cfg.WIN_HEIGHT - 2: # especific area condition
            if self.grabbing: cfg.DISPLAYSURF.blit(self.assets[2], (self.pos[0] + 2, self.pos[1] - 8))
            cfg.DISPLAYSURF.blit(self.assets[self.current_state], self.pos)

    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: self.clicking = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: self.clicking = False
