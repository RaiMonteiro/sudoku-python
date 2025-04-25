import pygame
import json
from math import sqrt
from time import time
import scripts.config as cfg
from scripts.utils import writeText

class Lable:
    def __init__(self, objectCoordinates: tuple, text: str, font: pygame.font.Font): 
        self.coor = objectCoordinates
        self.text = text
        self.font = font
        self.rect = (self.coor[0], self.coor[1] - 40, self.font.size(self.text)[0] + 20, self.font.size(self.text)[1] + 10)
        self.surf = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.current_alpha, self.target_alpha = 0, 0
        self.show = False
        self.hover_start_time = None # to control the time of hover

    def fadeAnimation(self):
        if self.target_alpha > self.current_alpha: self.current_alpha = min(self.current_alpha + 20, self.target_alpha)
        elif self.target_alpha < self.current_alpha: self.current_alpha = max(self.current_alpha - 30, self.target_alpha)

    def setTargetAlpha(self, a: int):
        now = time()

        if a == 255:
            if self.hover_start_time is None:
                self.hover_start_time = now # sets the time
            elif now - self.hover_start_time >= 1: # delay
                self.target_alpha = a
        else:
            self.hover_start_time = None
            self.target_alpha = a

    def resetAlpha(self):
        self.current_alpha, self.target_alpha = 0, 0
        self.hover_start_time = None

    def update(self):
        self.fadeAnimation()
        if self.current_alpha != 0: self.show = True
        else: self.show = False

    def draw(self):
        self.update()
        if self.show:
            self.surf.fill((*cfg.BISQUE, self.current_alpha))
            pygame.draw.rect(self.surf, (*cfg.MARRON, self.current_alpha), (0, 0, self.rect[2], self.rect[3]), 2)
            writeText(self.surf, self.font, self.text, cfg.DARKBROWN, (10, 5), self.current_alpha)
            cfg.DISPLAYSURF.blit(self.surf, (self.rect[0], self.rect[1]))

class InputButtonToNotes:
    def __init__(self):
        self.updating = True
        self.current_version = self.getVersion()
        self.text = f'Versão: {self.current_version}'
        self.rect_x, self.rect_y, self.rect_w, self.rect_h = 20, 750, 0, 0
        self.color = cfg.WHITE
        self.pressed = False
        self.lable = object()

    def getVersion(self):
        with open("source/r_notes/notes.json", mode="r", encoding="utf-8") as file: notes_data = json.load(file)
        return notes_data["update"][len(notes_data["update"]) - 1]["version"]
    
    def update(self):
        if self.rect_w == 0 and self.rect_h == 0:
            self.rect_w, self.rect_h = cfg.FONT_CFG[0].size(self.text)
            self.lable = Lable((self.rect_x, self.rect_y), "Clique aqui para ver todas as atualizações", cfg.FONT_CFG[4])
        
        if self.isHover():
            self.color = cfg.BISQUE
            self.lable.setTargetAlpha(255)
        else:
            self.color = cfg.WHITE
            self.lable.setTargetAlpha(0)

    def draw(self):
        if self.updating: self.update()
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], self.text, self.color, (self.rect_x, self.rect_y))
        self.lable.draw()

    def isHover(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0] >= self.rect_x and mouse_pos[0] <= self.rect_x + self.rect_w and mouse_pos[1] >= self.rect_y and mouse_pos[1] <= self.rect_y + self.rect_h
    
    def eventHandler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.isHover(): self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.isHover() and self.pressed:
            self.updating = False
            self.lable.resetAlpha()
            cfg.releasenotes.render = True

class Notes:
    def __init__(self):
        self.render = False
        self.bg_alpha_surface = pygame.Surface((cfg.WIN_WIDTH, cfg.WIN_HEIGHT), pygame.SRCALPHA)
        self.content = ContentDisplayment()
        self.exit_button = ExitButton() # exit button
        self.all_versions = list() # list of all versions buttons
        self.released_notes = list() # list of all released notes
        self.current_notes_index = None # identifies which released note is being displayed

        # loads all the information from the json file and saves it in variables
        with open("source/r_notes/notes.json", mode="r", encoding="utf-8") as file: self.notes = json.load(file)

        for i in range(len(self.notes["update"])):
            self.all_versions.append(VersionButton(i, self.notes["update"][i]["version"]))
            self.released_notes.append(self.notes["update"][i]["release_notes"])

        if self.current_notes_index != None:
            self.notes["update"][self.current_notes_index]["active"] = True
        else:
            self.current_notes_index = len(self.all_versions) - 1
            self.notes["update"][self.current_notes_index]["active"] = True

            if self.notes["update"][self.current_notes_index]["new"] == True:
                self.render = True

        self.all_versions[self.current_notes_index].active = True

    def lastUpdatesAside(self):
        # last updates title
        l_updates_t_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        l_updates_t_surf.fill((20, 53, 99, 180))
        cfg.DISPLAYSURF.blit(l_updates_t_surf, (50, 50))
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], "Versões lançadas", cfg.WHITE, (65, 60))
        
        # manages all the past versions buttons
        for btn in self.all_versions:
            # ensures that only one button can be active
            if btn.active and btn.listIndex != self.current_notes_index: # it correspond to the new active button
                # searches for the old activated button
                for _ in self.all_versions:
                    if _.active and _.listIndex == self.current_notes_index:
                        _.active = False
            # draws the button
            btn.draw()

    def display(self):
        self.bg_alpha_surface.fill((34, 63, 103, 220))
        cfg.DISPLAYSURF.blit(self.bg_alpha_surface, (0, 0))

        self.lastUpdatesAside()
        self.content.display()
        self.exit_button.draw()

    def exit(self):
        self.render = False
        cfg.releasenotes_btn.updating = True
        self.current_notes_index = None
        self.all_versions[-1].active = True
        self.notes["update"][-1]["new"] = False
        # rewrite the json file with the new information
        with open("source/r_notes/notes.json", mode="w", encoding="utf-8") as file: json.dump(self.notes, file, indent=4, ensure_ascii=False)
        self.content.reset() # resets the starting position

class ContentDisplayment:
    def __init__(self):
        self.content = None
        # container rect for content displayment
        self.content_start_x, self.content_start_y, self.content_width, self.content_height = (300, 250, 850, 0) # content_height = 0 to indicate that the height should be stored here
        # text printing positions
        self.text_x_pos, self.text_y_pos = self.content_start_x, self.content_start_y
        self.scroll = ScrollBar()

    def textAlphaCalculation(self, y_pos: int):
        initial_fade_pos, final_fade_pos = 265, 710

        if y_pos < initial_fade_pos:
            alpha = 255 - (initial_fade_pos - y_pos) * 10
            if alpha < 0: alpha = 0
            return alpha
        elif y_pos > final_fade_pos:
            alpha = 255 - (y_pos - final_fade_pos) * 10
            if alpha < 0: alpha = 0
            return alpha
        else: return 255
        
    # different text formatations
    def titleFormat(self, string: str):
        self.text_x_pos = self.content_start_x
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], string, cfg.WHITE, (self.text_x_pos, self.text_y_pos), self.textAlphaCalculation(self.text_y_pos), True)
        self.text_y_pos += cfg.FONT_CFG[0].get_linesize() + 10

    def textFormat(self, string: str):
        self.text_x_pos = self.content_start_x + 20
        text = string.split("\n")
        for line in text:
            writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[5], line, cfg.WHITE, (self.text_x_pos, self.text_y_pos), self.textAlphaCalculation(self.text_y_pos))
            self.text_y_pos += cfg.FONT_CFG[5].get_linesize()

    def pointFormat(self, string: str):
        self.text_x_pos = self.content_start_x + 20
        # creates a list point with alpha calculation
        circle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(circle_surf, (*cfg.WHITE, self.textAlphaCalculation(self.text_y_pos)), (3, 3), 3, 1)
        cfg.DISPLAYSURF.blit(circle_surf, (self.text_x_pos, self.text_y_pos + 10))
        
        text = string.split("\n")
        for line in text:
            writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[5], line, cfg.WHITE, (self.text_x_pos + 15, self.text_y_pos), self.textAlphaCalculation(self.text_y_pos))
            self.text_y_pos += cfg.FONT_CFG[5].get_linesize()

    def noteFormat(self, string: str):
        self.text_x_pos = self.content_start_x
        self.text_y_pos += 20
        text = string.split("\n")
        for line in text:
            writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[4], line, cfg.BLACK, (self.text_x_pos, self.text_y_pos), self.textAlphaCalculation(self.text_y_pos))
            self.text_y_pos += cfg.FONT_CFG[4].get_linesize()
        self.text_y_pos += cfg.FONT_CFG[4].get_linesize() + 20

    def update(self):
        # updates the current content dynamiclly
        if self.content != cfg.releasenotes.released_notes[cfg.releasenotes.current_notes_index]:
            self.content = cfg.releasenotes.released_notes[cfg.releasenotes.current_notes_index]
            self.content_start_y, self.content_height = 250, 0

    def display(self):
        self.update()
        # creates a surface for the header
        header_surf = pygame.Surface((850, 200), pygame.SRCALPHA)
        header_surf.fill((20, 53, 99, 180))
        cfg.DISPLAYSURF.blit(header_surf, (300, 50)) # draws the surface
        # header text
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[3], self.content["title"], cfg.WHITE, (350, 80))
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], self.content["date"], cfg.WHITE, (350, 180))

        # content display
        for para in range(len(self.content["content"])):
            self.text_y_pos += 30 # each paragraph adds a space between the content
            for line in range(len(self.content["content"][para])):
                match self.content["content"][para][line][0]:
                    case "title": self.titleFormat(self.content["content"][para][line][1])
                    case "text": self.textFormat(self.content["content"][para][line][1])
                    case "point": self.pointFormat(self.content["content"][para][line][1])
                    case "note": self.noteFormat(self.content["content"][para][line][1])

        # updates the total height dynamically, after first text rendering
        if self.content_height == 0:
            if self.text_y_pos > self.content_height:
                self.content_height = self.text_y_pos - self.content_start_y
            else: self.content_height = 500 # minimum content height

        self.text_x_pos, self.text_y_pos = self.content_start_x, self.content_start_y # resets the text positions

        self.scroll.draw()

    def reset(self):
        self.content_start_y = 250
        self.scroll.y_pos = 0

class ScrollBar:
    def __init__(self):
        self.content_h = 0
        self.scrollbar_h, self.view_h = 500, 500
        self.handler_w, self.handler_h = 15, 0
        self.handler_left_space, self.view_left_space = 0, 0 # represent the spaces that aren't occupied
        self.x_pos, self.y_pos = 0, 0

        self.surf = pygame.Surface((self.handler_w, self.scrollbar_h), pygame.SRCALPHA)
        self.top_left_origin = (1135, 250) # starting point of the surface
        self.current_alpha, self.target_alpha = 0, 0

        # mouse interactions
        self.close_range_mouse = False
        self.hover = False
        self.pressed = False
        self.y_distance_from_mouse = None # saves the distance between the mouse position to the top y position of the scroll bar

        # mouse wheel interaction
        self.mouse_wheel_scrolling = False
        self.mouse_wheel_movement = 0

    def update(self):
        # updates the sizes automaticly
        if self.content_h != cfg.releasenotes.content.content_height:
            self.handler_left_space, self.view_left_space = 0, 0 # resets values ​​to avoid calculation errors
            self.y_pos = 0
            self.current_alpha, self.target_alpha = 0, 0
            if cfg.releasenotes.content.content_height > self.view_h:
                self.content_h = cfg.releasenotes.content.content_height # content size
                self.handler_h = round((self.scrollbar_h / self.content_h) * self.view_h) # calculate the handler ratio
                self.view_left_space = self.content_h - self.view_h
                self.handler_left_space = self.scrollbar_h - self.handler_h
            else:
                self.content_h = self.view_h
                self.handler_h = 0
        else:
            if self.content_h > self.view_h:
                cfg.releasenotes.content.content_start_y = 250 - ((self.y_pos / self.handler_left_space) * self.view_left_space) # updates the content position, using a ratio calculation
                self.fadeAnimation()

        # ensures that the scroll bar does not go beyond its limits
        if not self.mouse_wheel_scrolling:
            # mouse interactions
            if self.pressed and not self.close_range_mouse and not self.hover: self.pressed = False

            mouse_pos = pygame.mouse.get_pos()
            if self.isInSight(mouse_pos) and self.pressed:
                new_pos = (mouse_pos[1] - self.y_distance_from_mouse) - self.top_left_origin[1]
                if new_pos >= 0 and new_pos + self.handler_h <= self.scrollbar_h: self.y_pos = new_pos
                elif new_pos < 0: self.y_pos = 0
                elif new_pos + self.handler_h > self.scrollbar_h: self.y_pos = self.scrollbar_h - self.handler_h
        else:
            # mouse wheel interactions
            new_pos = self.y_pos - self.mouse_wheel_movement
            if new_pos >= 0 and new_pos + self.handler_h <= self.scrollbar_h: self.y_pos = new_pos
            elif new_pos < 0: self.y_pos = 0
            elif new_pos + self.handler_h > self.scrollbar_h: self.y_pos = self.scrollbar_h - self.handler_h

            # resets the values ​​so there are no successive increments
            self.mouse_wheel_scrolling = False
            self.mouse_wheel_movement = 0

    def draw(self):
        self.update()
        if self.content_h > self.view_h: # draws if necessary
            self.surf.fill((0, 0, 0, 0)) # clears the surface
            pygame.draw.rect(self.surf, (255, 255, 255, self.current_alpha), (self.x_pos, self.y_pos, self.handler_w, self.handler_h))
            pygame.draw.line(self.surf, (0, 0, 0, 50), (0, 0), (0, self.scrollbar_h))
            cfg.DISPLAYSURF.blit(self.surf, self.top_left_origin)

    def fadeAnimation(self):
        if self.current_alpha != self.target_alpha:
            if self.current_alpha < self.target_alpha: self.current_alpha = min(self.current_alpha + 5, self.target_alpha, 255)
            else: self.current_alpha = max(self.current_alpha - 2, self.target_alpha, 0)

    def isInSight(self, m_pos: tuple):
        if m_pos[0] >= self.top_left_origin[0] - 850 and m_pos[0] <= self.top_left_origin[0] + self.handler_w + 20 and m_pos[1] >= self.top_left_origin[1] and m_pos[1] <= self.top_left_origin[1] + self.view_h: # content area validation
            self.close_range_mouse = False
            self.hover = False
            self.target_alpha = 50

            if m_pos[0] >= self.top_left_origin[0] - 200 and m_pos[0] <= self.top_left_origin[0] + self.handler_w + 20 and m_pos[1] >= self.top_left_origin[1] and m_pos[1] <= self.top_left_origin[1] + self.view_h: # close range area validation
                self.close_range_mouse = True

                if m_pos[0] >= self.top_left_origin[0] and m_pos[0] <= self.top_left_origin[0] + self.handler_w and m_pos[1] >= self.top_left_origin[1] + self.y_pos and m_pos[1] <= self.top_left_origin[1] + self.y_pos + self.handler_h: # hover area validation
                    self.hover = True
                    self.target_alpha = 100
        else:
            # it is not in sight at all
            self.close_range_mouse = False
            self.hover = False
            self.target_alpha = 0
            return False
        return True

    def calculateDistance(self):
        mouse_pos_y = pygame.mouse.get_pos()
        self.y_distance_from_mouse = mouse_pos_y[1] - (self.top_left_origin[1] + self.y_pos)

    def eventHandler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed and self.hover:
            self.pressed = True
            self.calculateDistance()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed:
            self.pressed = False
            self.y_distance_from_mouse = None

        if not self.pressed:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEWHEEL and self.isInSight(mouse_pos):
                self.mouse_wheel_scrolling = True
                self.mouse_wheel_movement = int(event.precise_y * 10)

class VersionButton:
    def __init__(self, listIndex: int, text: str):
        self.listIndex = listIndex
        self.text = text
        self.pos_x, self.pos_y = (50, 100 + (50 * self.listIndex))
        self.surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        self.surf_color = (34, 63, 103)
        self.alpha = 100
        self.pressed = False
        self.active = False

    def update(self):
        if self.active and cfg.releasenotes.current_notes_index != self.listIndex: cfg.releasenotes.current_notes_index = self.listIndex # when the active state changes due to human interactions
            
        # manages the alpha values
        if self.active: self.alpha = 255
        elif self.isHover():
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

    def eventHandler(self, event: pygame.event.Event):
        if self.isHover():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed:
                self.pressed = False
                self.active = True
        else: self.pressed = False

class ExitButton:
    def __init__(self):
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.top_left_origin = (1125, 25)
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
        writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], "x", cfg.WHITE, (self.top_left_origin[0] + 15, self.top_left_origin[1] - 5), self.text_alpha) # specific location for the text

    def isHover(self):
        mouse_pos = pygame.mouse.get_pos()
        circle_center = (self.top_left_origin[0] + self.radius, self.top_left_origin[1] + self.radius) # defines the center of the circle for better understanding
        distance = sqrt((mouse_pos[0] - circle_center[0])**2 + (mouse_pos[1] - circle_center[1])**2) # distance formula using the Pythagorean theorem
        return distance <= self.radius

    def eventHandler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.isHover(): self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.isHover() and self.pressed:
            self.pressed = False
            cfg.releasenotes.exit()