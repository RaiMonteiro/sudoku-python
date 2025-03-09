import pygame
import json
from math import sqrt
import config as cfg
from utils import writeText

class Notes:
    def __init__(self):
        self.render = True
        self.button_alpha_surface = pygame.Surface((cfg.WIN_WIDTH, cfg.WIN_HEIGHT), pygame.SRCALPHA)
        self.exit_button = ExitButton() # exit button
        self.all_versions = list() # list of all versions buttons

        # creates and defines the versions buttons from the json file
        with open("src/r_notes/notes.json", mode="r", encoding="utf-8") as file: notes = json.load(file)
        for i in range(len(notes["update"])): self.all_versions.append(VersionButton(i, notes["update"][i]["version"]))
            

    
    def lastUpdatesAside(self):
        # pygame.draw.rect(cfg.DISPLAYSURF, cfg.MARRON, (50, 50, 200, 50), 1, 0) # aside titulo
        l_updates_t_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        l_updates_t_surf.fill((34, 63, 103, 180))
        cfg.DISPLAYSURF.blit(l_updates_t_surf, (50, 50))
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], "Versões lançadas", cfg.WHITE, (65, 60))

        # pygame.draw.rect(cfg.DISPLAYSURF, cfg.RED, (50, 100, 200, 650), 1, 0) # aside conteudo
        
        for btn in self.all_versions: btn.draw() # draws all the buttons
        



    def content(self):
        def titleDisplay(title: str, date: str):
            new_surf = pygame.Surface((850, 200), pygame.SRCALPHA)
            new_surf.fill((34, 63, 103, 180))
            cfg.DISPLAYSURF.blit(new_surf, (300, 50))

            # pygame.draw.rect(cfg.DISPLAYSURF, cfg.MARRON, (300, 50, 850, 200), 1, 0) # titulo
            writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[3], title, cfg.WHITE, (350, 80))
            writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], date, cfg.WHITE, (350, 180))

        with open("src/r_notes/notes.json", mode="r", encoding="utf-8") as file:
            notes = json.load(file)
            r_notes = notes["update"][0]["release_notes"]

        titleDisplay(r_notes["title"], r_notes["date"])

        pygame.draw.rect(cfg.DISPLAYSURF, cfg.RED, (300, 250, 850, 500), 1, 0) # conteudo

    def display(self):
        self.button_alpha_surface.fill((34, 63, 103, 220))
        cfg.DISPLAYSURF.blit(self.button_alpha_surface, (0, 0))

        # pygame.draw.rect(cfg.DISPLAYSURF, cfg.WHITE, (50, 50, 1100, 700), 1, 0) # container
        self.lastUpdatesAside()
        self.content()
        self.exit_button.draw()

        

        # texto
        # u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[3], "Notas de lançamento", cfg.WHITE, (100, 50))

class VersionButton:
    def __init__(self, listIndex: int, text: str):
        self.listIndex = listIndex
        self.text = text
        self.pos_x, self.pos_y = (50, 100 + (50 * self.listIndex))
        self.surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        self.surf_color = (34, 63, 103)
        self.alpha = 100
        self.pressed = False

    def update(self):
        if self.isHover():
            if self.pressed: self.alpha = 255
            else: self.alpha = 200
        else: self.alpha = 100

    def draw(self):
        self.update()
        self.surf.fill((*self.surf_color, self.alpha))
        cfg.DISPLAYSURF.blit(self.surf, (self.pos_x, self.pos_y))
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[4], self.text, cfg.WHITE, (65, 115 + (50 * self.listIndex)))

    def isHover(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0] >= self.pos_x and mouse_pos[0] <= self.pos_x + 200 and mouse_pos[1] >= self.pos_y and mouse_pos[1] <= self.pos_y + 50

    def eventHandler(self, event):
        if self.isHover():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed:
                self.pressed = False

class ExitButton:
    def __init__(self):
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.top_left_origin = (1100, 50)
        self.radius = 25
        self.button_alpha = 50
        self.text_alpha = 200
        self.pressed = False
    
    def update(self):
        # manages the alpha values
        if self.isHover():
            if self.pressed:
                self.button_alpha = 180
            else:
                self.button_alpha = 100
                self.text_alpha = 255
        else:
            self.button_alpha = 50
            self.text_alpha = 200

    def draw(self):
        self.update()
        pygame.draw.circle(self.surf, (0, 34, 80, self.button_alpha), (25, 25), self.radius)
        cfg.DISPLAYSURF.blit(self.surf, self.top_left_origin)
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], "x", cfg.WHITE, (1115, 45), self.text_alpha) # specific location for the text

    def isHover(self):
        mouse_pos = pygame.mouse.get_pos()
        circle_center = (self.top_left_origin[0] + self.radius, self.top_left_origin[1] + self.radius) # defines the center of the circle for better understanding
        distance = sqrt((mouse_pos[0] - circle_center[0])**2 + (mouse_pos[1] - circle_center[1])**2) # distance formula using the Pythagorean theorem
        return distance <= self.radius

    def eventHandler(self, event):
        if self.isHover():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed:
                self.pressed = False

