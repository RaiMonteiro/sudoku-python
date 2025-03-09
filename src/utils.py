# Reusable code for all modules
import sys, pygame, random
import time as t
import config as cfg
    
class StateManager: # stores, changes and runs the current state and executes the given scene
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.temp_name_state = None

    def addState(self, name, func):
        self.states[name] = func

    def changeState(self, name):
        self.current_state = self.states.get(name)
        if self.current_state == None: self.temp_name_state = name

    def runCurrentState(self):
        if self.current_state:
            self.temp_name_state = None
            self.current_state()

class Centralize: # centralize the items regarding the "parent-box" 
    def __init__(self, coor, boxSize, itemSize):
        self.x, self.y = coor
        self.box_w, self.box_h = boxSize
        self.item_w, self.item_h = itemSize

    def xAxis(self):
        return self.x + ((self.box_w / 2) - (self.item_w / 2))

    def yAxis(self):
        return self.y + ((self.box_h / 2) - (self.item_h / 2))

class Timer:
    def __init__(self):
        self.changed = False
        self.time = [0, 0, 0]
        self.start = t.time()
        
    def update(self):
        now = t.time()
        if now - self.start >= 1:
            self.time[2] += 1
            self.start = now
            self.changed = True
        else: self.changed = False

        if self.time[2] == 60:
            self.time[1] += 1
            self.time[2] = 0

        if self.time[1] == 60:
            self.time[0] += 1
            self.time[1] = 0
            self.time[2] = 0
    
    def toStr(self):
        hours = f'0{self.time[0]}' if self.time[0] < 10 else self.time[0]
        minutes = f'0{self.time[1]}' if self.time[1] < 10 else self.time[1]
        seconds = f'0{self.time[2]}' if self.time[2] < 10 else self.time[2]
        if self.time[0] > 0: return f'{hours} : {minutes} : {seconds}'
        else: return f'{minutes} : {seconds}'

    def delay(self, seconds: float): t.sleep(seconds)
    
    def reset(self):
        self.changed = False
        self.time = [0, 0, 0]

def close(): # exit the program
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

def setBg(index, pos = (0, 0), animation = False): # draw the background
    if not animation:
        try: cfg.ASSETS[index].render(loop=False)
        except: cfg.DISPLAYSURF.blit(cfg.ASSETS[index], pos)
    else: cfg.ASSETS[index].render(loop=True)

def drawObjects(*args): # draws the objects from a given array
    for i in range(len(args)):
        for obj in args[i]:
            obj.draw()

def writeText(surf, font, text, color, coor, alpha = 255):
    text = font.render(text, True, (*color, alpha))
    text.set_alpha(alpha)
    surf.blit(text, coor)

def inputHandler(shutdown = True, buttons = None, blocks = None): # manages the user's inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if shutdown: close()
            else:
                cfg.manager.changeState("sd")
                return "pressed"

        cfg.c.eventHandler(event) # cursor event handler

        if buttons != None:
            for btn in buttons:
                btn.eventHandler(event)
                if btn.change_state: return "pressed"

        if blocks != None:
            for b in blocks: 
                b.mouseInteractions(event)
                if b.delete: 
                    cfg.blcs.remove(b)
                    del b

        # for gameRequirements function
        if cfg.manager.temp_name_state == "user_name":
            if event.type == pygame.TEXTINPUT and len(cfg.user_name) < 12:
                if event.text.isalnum():
                    cfg.user_name += event.text

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    cfg.user_name = cfg.user_name[:-1]
                if event.key == pygame.K_SPACE and len(cfg.user_name) < 12:
                    cfg.user_name += " "

        # for releaseNotes events handlers
        if cfg.updatenotes.render:
            cfg.updatenotes.exit_button.eventHandler(event)
            for b in cfg.updatenotes.all_versions: b.eventHandler(event)


    # Sujeito a ser retirado    
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        close()

def shuffle(list):
    for i in range(8, 0, -1):
        r = random.randint(0, i)
        temp = list[i]
        list[i] = list[r]
        list[r] = temp

def defualtGameVars(): # resets all the game variables
    cfg.sudoku["solved"] = [[0 for _ in range(9)] for _ in range(9)]
    cfg.sudoku["maped"] = [[0 for _ in range(9)] for _ in range(9)]
    cfg.sudoku["static"] = [[0 for _ in range(9)] for _ in range(9)]
    cfg.subgrid_d = [1 for _ in range(9)]
    cfg.user_name = str()
    cfg.level = None
    cfg.timer.reset()
    cfg.errors = 0
    cfg.current_pts = None

# Para eliminar
def cheat():
    print("Sudoku resolvido")
    for i in range(9):
        print(*cfg.sudoku["solved"][i])
        
    print("----------------------")
    print("Sudoku visivel")
    for i in range(9):
        print(*cfg.sudoku["maped"][i])