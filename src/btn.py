import pygame
import config as cfg
from utils import Centralize

class Button:
    def __init__(self, surf, text, rectValues, depth, func):
        self.surf = surf
        self.text = text
        self.size_px_x, self.size_px_y = cfg.FONT_CFG[1].size(self.text)
        self.x, self.y, self.width, self.height = rectValues
        self.depth = depth

        self.asset = pygame.transform.scale(cfg.ASSETS[5], (self.width, self.height))
        self.asset_pos_x, self.asset_pos_y = (self.x, self.y - self.depth)

        self.state_func = func
        self.change_state = False
        self.hovered = False
        self.active = False

        if self.width < self.size_px_x: self.width = self.size_px_x + 100
    
    def update(self):
        if self.active and not self.hovered: self.active = False
        if self.active: self.asset_pos_y = self.y
        else: self.asset_pos_y = self.y - self.depth

    def draw(self):
        self.update()
        text_centralized = Centralize((self.asset_pos_x, self.asset_pos_y), (self.width, self.height), (self.size_px_x, self.size_px_y))
        pygame.draw.rect(self.surf, cfg.DARKBROWN, (self.x, self.y, self.width, self.height), 0, 15) # button depth
        if self.hovered:
            self.surf.blit(self.asset, (self.asset_pos_x, self.asset_pos_y))
            self.surf.blit(cfg.FONT_CFG[1].render(self.text, True, cfg.WHITE), (text_centralized.xAxis(), text_centralized.yAxis()))
        else:
            self.surf.blit(self.asset, (self.asset_pos_x, self.asset_pos_y))
            self.surf.blit(cfg.FONT_CFG[1].render(self.text, True, cfg.BLACK), (text_centralized.xAxis(), text_centralized.yAxis()))

    def hover_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = True if mouse_pos[0] >= self.asset_pos_x and mouse_pos[0] <= self.asset_pos_x + self.width and mouse_pos[1] >= self.asset_pos_y and mouse_pos[1] <= self.asset_pos_y + self.height else False
    
    def eventHandler(self, event):
        self.hover_handler()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            cfg.SOUNDS[0].play()
            self.active = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.hovered and self.active:
            cfg.SOUNDS[1].play()
            self.active = False
            self.change_state = True
            cfg.manager.changeState(self.state_func)