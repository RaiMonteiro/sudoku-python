# ---------------- Sudoku Game by ------------------ #
# Francisco Raí Alves Ribães Monteiro, aka Cisco2000 #
# -- Just a college student making games for fun --- #
# ---- Only the portuguese version is available ---- #
# ------------------ fev. 2025 --------------------- #
import pygame, random
import config as cfg
import utils as u
import stats as stats
from btn import Button
from block import Block
# import sys
# import memorytest as mt # para testar a memoria

def main():
    pygame.init()
    pygame.mixer.init()
    cfg.DISPLAYSURF = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
    cfg.FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(cfg.ASSETS[7])

    cfg.FONT_CFG = [
        pygame.font.Font("./assets/font/YatraOne-Regular.ttf", 20),
        pygame.font.Font("./assets/font/YatraOne-Regular.ttf", 30),
        pygame.font.Font("./assets/font/YatraOne-Regular.ttf", 40),
        pygame.font.Font("./assets/font/YatraOne-Regular.ttf", 80),
        pygame.font.Font("./assets/font/YatraOne-Regular.ttf", 15)
    ]

    cfg.SOUNDS = [
        pygame.mixer.Sound("./assets/sounds/buttonEvents/click-down.wav"),
        pygame.mixer.Sound("./assets/sounds/buttonEvents/click-up.wav"),
        pygame.mixer.Sound("./assets/sounds/block-drop.wav"),
        pygame.mixer.Sound("./assets/sounds/end-game.wav"),
        pygame.mixer.Sound("./assets/sounds/wrong.wav")
    ]

    pygame.mixer.music.load("./assets/sounds/Shigeo-Sekito-the-word-II.mp3")
    pygame.mixer.music.play(-1)

    while True:
        cfg.manager.runCurrentState()
 
def menu():
    cfg.btns = [
        Button(cfg.DISPLAYSURF, "Jogar", (700, 300, 300, 70), 10, "game_req"),
        Button(cfg.DISPLAYSURF, "Pontuações", (700, 400, 300, 70), 10, "score_table"),
        Button(cfg.DISPLAYSURF, "Sair", (700, 500, 300, 70), 10, "exit")
    ]
    v = stats.getVersion()
    u.defualtGameVars()

    while True:
        u.setBg(0, animation=True)
        cfg.DISPLAYSURF.blit(cfg.ASSETS[6], (200, 300)) # logo        
        u.drawObjects(cfg.btns)
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], f'Versão: {v}', cfg.WHITE, (20, 750)) # displays the current version
        cfg.particles.leaFall()
        cfg.particles.drawAll()
        cfg.c.showCursor()
        pygame.display.flip()

        if u.inputHandler(buttons = cfg.btns) == "pressed":
            cfg.particles.removeAll()
            return
        cfg.FPSCLOCK.tick(cfg.FPS)

def shutdownPopUp():
    cfg.btns = [
        Button(cfg.DISPLAYSURF, "Retomar", (370, 365, 200, 70), 10, "game"),
        Button(cfg.DISPLAYSURF, "Sair", (630, 365, 200, 70), 10, "exit")
    ]
    while True:
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1, (20, 20))
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], "Pretende sair do jogo?", cfg.WHITE, (380, 220))
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], "Todos os dados não guardados serão perdidos", cfg.RED, (370.5, 280))
        u.drawObjects(cfg.btns)
        cfg.c.showCursor()
        pygame.display.flip()
        if u.inputHandler(False, cfg.btns) == "pressed": return
        cfg.FPSCLOCK.tick(cfg.FPS)

def gamePaused():
    cfg.btns = [Button(cfg.DISPLAYSURF, "Menu", (370, 365, 200, 70), 10, "menu"), Button(cfg.DISPLAYSURF, "Retomar", (630, 365, 200, 70), 10, "game")]
    while True:
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1)
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[3], "Em Pausa", cfg.WHITE, (411, 200))
        u.drawObjects(cfg.btns)
        cfg.c.showCursor()
        pygame.display.flip()

        if u.inputHandler(False, cfg.btns) == "pressed": return
        cfg.FPSCLOCK.tick(cfg.FPS)

def gameHelp():
    pass

def gameRequirements():
    cfg.btns = [
        Button(cfg.DISPLAYSURF, "Fácil", (510, 365, 180, 50), 10, "0"),
        Button(cfg.DISPLAYSURF, "Médio", (510, 435, 180, 50), 10, "1"),
        Button(cfg.DISPLAYSURF, "Difícil", (510, 505, 180, 50), 10, "2")
    ]

    while True: # defines the difficulty level
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1)
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[1], "Nível de Dificuldade", cfg.WHITE, (456.5, 270))
        u.drawObjects(cfg.btns)
        cfg.c.showCursor()
        pygame.display.flip()

        if u.inputHandler(True, cfg.btns) == "pressed":
            cfg.level = int(cfg.manager.temp_name_state) # the level takes a value from the button state
            cfg.current_pts = cfg.DIFFICULTY[cfg.level][3]
            cfg.btns = [Button(cfg.DISPLAYSURF, "Pronto", (510, 505, 180, 50), 10, "game")]
            break
        cfg.FPSCLOCK.tick(cfg.FPS)

    cfg.manager.changeState("user_name")
    pygame.key.start_text_input()
    while True: # defines user's name 
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1)
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[1], "Nome", cfg.WHITE, (558, 250))

        if len(cfg.user_name) > 0:
            # the name is always in the center
            name_centralized = u.Centralize((450, 360), (300, 80), cfg.FONT_CFG[2].size(cfg.user_name))
            u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], cfg.user_name, cfg.WHITE, (name_centralized.xAxis(), name_centralized.yAxis()))

        u.drawObjects(cfg.btns)
        cfg.c.showCursor()
        pygame.display.flip()

        if u.inputHandler(True, cfg.btns) == "pressed":
            pygame.key.stop_text_input()
            if len(cfg.user_name) == 0: cfg.user_name = "Sem Nome"
            return

        cfg.FPSCLOCK.tick(cfg.FPS)

def game():
    playing = True
    cfg.btns = [Button(cfg.DISPLAYSURF, "Pausar", (770, 280, 180, 70), 10, "game_pause"), Button(cfg.DISPLAYSURF, "?", (970, 280, 180, 70), 10, "game_help")]

    def graphics():
        x_table, y_table, thickness = 50, 50, 10
        x_increase, y_increase = 0, 0

        u.setBg(0)
        # game board
        cfg.DISPLAYSURF.blit(cfg.ASSETS[2], (40, 40))
        for i in range(9):
            if i == 3 or i == 6: y_increase += thickness
            for o in range(9):
                if o == 3 or o == 6: x_increase += thickness
                if cfg.sudoku["static"][i][o] > 0:
                    text_centralized = u.Centralize((x_table + x_increase + (cfg.CELL_SIZE * o), y_table + y_increase + (cfg.CELL_SIZE * i)), (60, 60), cfg.FONT_CFG[1].size(str(cfg.sudoku["static"][i][o])))
                    cfg.DISPLAYSURF.blit(cfg.ASSETS[4], (x_table + x_increase + (cfg.CELL_SIZE * o), y_table + y_increase + (cfg.CELL_SIZE * i)))
                    cfg.DISPLAYSURF.blit(cfg.FONT_CFG[2].render(str(cfg.sudoku["static"][i][o]), True, cfg.DARKBROWN), (text_centralized.xAxis(), text_centralized.yAxis()))
            x_increase = 0

        # timer box display
        cfg.DISPLAYSURF.blit(cfg.ASSETS[3], (770, 40))
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], f'Dificuldade: {cfg.DIFFICULTY[cfg.level][0]}', cfg.BLACK, (800, 55)) # aside left
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], f'Erros: {cfg.errors}/3', cfg.BLACK, (1020, 55)) # aside right
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], "Cronómetro", cfg.BLACK, (u.Centralize((770, 70), (380, 160), cfg.FONT_CFG[2].size("Cronómetro")).xAxis(), 110)) # timer
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], cfg.timer.toStr(), cfg.BLACK, (u.Centralize((770, 70), (380, 160), cfg.FONT_CFG[2].size(cfg.timer.toStr())).xAxis(), 170)) # time counter

        # block overlay adjustment
        for i in range(len(cfg.blcs)):
            if cfg.blcs[i].grabbed:
                cfg.blcs.append(cfg.blcs.pop(i)) # moves the grabbed block to the end of the list to be drawn last
                break

        # Objects
        u.drawObjects(cfg.btns, cfg.blcs)
        cfg.c.showCursor()
        pygame.display.flip()

    def subgridNumDisplay():
        remaining_cells = cfg.DIFFICULTY[cfg.level][2] - 9
        num_cells = cfg.DIFFICULTY[cfg.level][1]

        while remaining_cells > 0:
            for i in range(9):
            
                if remaining_cells > 0:
                    if remaining_cells < num_cells:
                        num = random.randint(1, remaining_cells)
                    else:
                        num = random.randint(1, num_cells - (1 + cfg.level))
                else: break

                if cfg.subgrid_d[i] + num <= num_cells:
                    cfg.subgrid_d[i] += num
                    remaining_cells -= num
                else: continue

        u.shuffle(cfg.subgrid_d)

        for i in range(9):
            subgrid_ln = int(i / 3) * 3
            subgrid_col = (i % 3) * 3
            visible_nums = cfg.subgrid_d[i]

            while visible_nums > 0:
                ln = random.randint(subgrid_ln, subgrid_ln + 2)
                col = random.randint(subgrid_col, subgrid_col + 2)

                if cfg.sudoku["maped"][ln][col] == 0:
                    cfg.sudoku["maped"][ln][col] = 10
                    visible_nums -= 1

    def validNumber(ln, col, n, grid): # checks if a number is not repeated
        for i in range(9):
            if grid[ln][i] == n or grid[i][col] == n or grid[int(ln / 3) * 3 + int(i / 3)][int(col / 3) * 3 + (i % 3)] == n: return False
        return True
    
    def generateCompleteGrid(grid): # generates a resoluble sudoku
        _list = [1, 2, 3, 4, 5, 6, 7, 8, 9] # list the possible numbers
        for ln in range(9):
            for col in range(9):
                if grid[ln][col] == 0:
                    u.shuffle(_list) # shuffling reduce the number of attempts

                    for i in range(9):
                        if validNumber(ln, col, _list[i], grid):
                            grid[ln][col] = _list[i]

                            if generateCompleteGrid(grid):
                                return True # tries to fill the remaining numbers
                            
                            grid[ln][col] = 0 # if it fail resets the cell value

                    return False # no valid number and go back
                
        return True # grid is complete

    def generateSudoku():
        generate = True
        for i in range(9):
            for j in range(9):
                if cfg.sudoku["maped"][i][j] != 0:
                    generate = False
                    break

        if generate:
            subgridNumDisplay()

            if generateCompleteGrid(cfg.sudoku["solved"]):
                for i in range(9):
                    for o in range(9):
                        if cfg.sudoku["maped"][i][o] == 10:
                            cfg.sudoku["maped"][i][o] = cfg.sudoku["solved"][i][o]
                            cfg.sudoku["static"][i][o] = cfg.sudoku["solved"][i][o]

            cfg.blcs = [Block((835, 400), 1), Block((925, 400), 2), Block((1015, 400), 3), Block((835, 490), 4), Block((925, 490), 5), Block((1015, 490), 6), Block((835, 580), 7), Block((925, 580), 8), Block((1015, 580), 9)]

    def checkingErrors(ln, col):
        nonlocal playing
        _num = cfg.sudoku["maped"][ln][col] # saves the number temporarily
        cfg.sudoku["maped"][ln][col] = 0 # resets the number
        if not validNumber(ln, col, _num, cfg.sudoku["maped"]):
            cfg.SOUNDS[4].play()
            cfg.errors += 1
            cfg.current_pts -= 200
            if cfg.errors == 3:
                playing = False
                cfg.current_pts = 0
            return True
        cfg.sudoku["maped"][ln][col] = _num # the grid coordinates get their number back
        return False

    def isGridCompleted():
        for i in range(9):
            for o in range(9):
                if cfg.sudoku["maped"][i][o] == 0: return False
        return True

    generateSudoku()

    # u.cheat()

    # game loop
    while True:
        graphics()

        if playing:
            cfg.timer.update()
            # upadates the current points
            if cfg.timer.changed:
                if cfg.current_pts > 0: cfg.current_pts -= 1
                else: cfg.current_pts = 0

            coor_copy = cfg.last_change.copy() # makes a copy to compare after the user's inputs
            if u.inputHandler(False, cfg.btns, cfg.blcs) == "pressed": return
            
            if cfg.last_change != coor_copy:
                if checkingErrors(cfg.last_change[0], cfg.last_change[1]) == False: # if there is no errors
                    # cheks if sudoku is completed after the errors verification
                    if isGridCompleted(): playing = False

        else:
            for b in cfg.blcs:
                # the end game should wait for the last block move
                if b.ref[0] == cfg.last_change[0] and b.ref[1] == cfg.last_change[1]:
                    if b.rest:
                        cfg.manager.changeState("game_end")
                        u.Timer().delay(2.0)
                        return
                    
        cfg.FPSCLOCK.tick(cfg.FPS)

def endGame():
    new_surf = pygame.Surface((cfg.WIN_WIDTH, cfg.WIN_HEIGHT), pygame.SRCALPHA)
    time_control = u.Timer()
    alpha = 0
    counter = 0
    if cfg.current_pts >= 60: add = cfg.current_pts / 60
    else: add = 1

    cfg.btns = [Button(cfg.DISPLAYSURF, "Continuar", (500, 650, 200, 70), 10, "menu")]

    # manipulating player data
    stats.add([cfg.user_name, cfg.DIFFICULTY[cfg.level][0], cfg.timer.toStr(), cfg.errors, cfg.current_pts])
    stats.arrange()

    # play sound
    cfg.SOUNDS[3].play()

    while True:
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1)
        new_surf.fill((0, 0, 0, 0))

        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[2], cfg.user_name, cfg.WHITE, (600 - cfg.FONT_CFG[2].size(cfg.user_name)[0] / 2, 150))
        u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[3], str(counter), cfg.WHITE, (600 - cfg.FONT_CFG[3].size(str(counter))[0] / 2, 200))

        u.writeText(new_surf, cfg.FONT_CFG[1], "Tempo", cfg.WHITE, (551, 350), alpha)
        u.writeText(new_surf, cfg.FONT_CFG[2], cfg.timer.toStr(), cfg.WHITE, (600 - cfg.FONT_CFG[2].size(cfg.timer.toStr())[0] / 2, 400), alpha)

        u.writeText(new_surf, cfg.FONT_CFG[1], "Dificuldade", cfg.WHITE, (600-300-80.5, 350), alpha)
        u.writeText(new_surf, cfg.FONT_CFG[2], cfg.DIFFICULTY[cfg.level][0], cfg.WHITE, (600-300 - cfg.FONT_CFG[2].size(cfg.DIFFICULTY[cfg.level][0])[0] / 2, 400), alpha)

        u.writeText(new_surf, cfg.FONT_CFG[1], "Erros", cfg.WHITE, (600+300-41.5, 350), alpha)
        u.writeText(new_surf, cfg.FONT_CFG[2], str(cfg.errors), cfg.WHITE, (600+300 - cfg.FONT_CFG[2].size(str(cfg.errors))[0] / 2, 400), alpha)
        if time_control.time[2] >= 3: u.drawObjects(cfg.btns) # draws the button after 3 seconds
        cfg.DISPLAYSURF.blit(new_surf, (0, 0)) # prints the new surface on the main surface
        cfg.c.showCursor()
        pygame.display.update()

        time_control.update()

        if time_control.time[2] == 20: # after 20 seconds the program jump to next scene
            cfg.manager.changeState("menu")
            return
        
        if u.inputHandler(True, cfg.btns) == "pressed": return

        # fade animation
        if alpha < 255: alpha += 5

        # points animation
        if counter < cfg.current_pts:
            if counter + int(add) > cfg.current_pts: add = cfg.current_pts - counter # to control the addition of numbers
            counter += int(add)

        cfg.FPSCLOCK.tick(cfg.FPS)

def scoreTable():
    x, y = (100, 70)
    box_w, box_h = (200, 50)
    players_data = stats.unboxData()
    cfg.btns = [Button(cfg.DISPLAYSURF, "Voltar", (cfg.WIN_WIDTH / 2 - 200 / 2, 650, 200, 70), 10, "menu")]

    while True:
        cfg.DISPLAYSURF.fill(cfg.BLACK)
        u.setBg(1)
        u.drawObjects(cfg.btns)

        # header
        for i in range(5):
            t_head = ["Nome", "Dificuldade", "Tempo", "Erros", "Pontuação"]
            text_centralized = u.Centralize((x + i * box_w, y), (box_w, box_h), cfg.FONT_CFG[1].size(t_head[i]))

            # pygame.draw.rect(cfg.DISPLAYSURF, cfg.WHITE, (x + i * box_w, y, box_w, box_h), 1, 0) #retirar

            u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[1], t_head[i], cfg.WHITE, (text_centralized.xAxis(), text_centralized.yAxis()))
        
        # body
        for i in range(10):
            for j in range(5):
                try:
                    text_centralized = u.Centralize((x + (box_w * j), (y + box_h) + (i * box_h)), (box_w, box_h), cfg.FONT_CFG[0].size(str(players_data[i][j])))
                    u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], str(players_data[i][j]), cfg.WHITE, (text_centralized.xAxis(), text_centralized.yAxis()))
                except:
                    text_centralized = u.Centralize((x + (box_w * j), (y + box_h) + (i * box_h)), (box_w, box_h), cfg.FONT_CFG[0].size("-"))
                    u.writeText(cfg.DISPLAYSURF, cfg.FONT_CFG[0], "-", cfg.WHITE, (text_centralized.xAxis(), text_centralized.yAxis()))
        cfg.c.showCursor()
        pygame.display.flip()

        if u.inputHandler(buttons = cfg.btns) == "pressed": return

        cfg.FPSCLOCK.tick(cfg.FPS)

if __name__ == "__main__":
    cfg.manager.addState("menu", menu)
    cfg.manager.addState("game", game)
    cfg.manager.addState("game_req", gameRequirements)
    cfg.manager.addState("game_pause", gamePaused)
    cfg.manager.addState("game_help", gameHelp)
    cfg.manager.addState("game_end", endGame)
    cfg.manager.addState("score_table", scoreTable)
    cfg.manager.addState("sd", shutdownPopUp)
    cfg.manager.addState("exit", u.close)

    cfg.manager.changeState("menu")
    # cfg.manager.changeState("game")
    # cfg.manager.changeState("game_req")
    # cfg.manager.changeState("game_end")
    # cfg.manager.changeState("score_table")
    # cfg.manager.changeState("sd")
    main()