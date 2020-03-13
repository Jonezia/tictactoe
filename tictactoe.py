import pygame
import time
pygame.init()

mainfont = pygame.font.SysFont('Roboto',70)
timefont = pygame.font.SysFont('Roboto', 30)

class Grid:    
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.Xpositions = []
        self.Opositions = []
        self.squares = [[Square(i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.win = win
        self.XO = "X"
        self.wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        
    def draw(self):
        gap = self.width / self.rows
        for i in range(self.rows+1):
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap))
            pygame.draw.line(self.win, (0,0,0), (i * gap, 0), (i * gap, self.height))
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.win)
    
    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.rows
            x = pos[0] // gap
            y = pos[1] // gap
            if self.squares[int(y)][int(x)].mark(self.XO):
                if self.XO == "X":
                    self.Xpositions.append(int(3*y+x))
                else:
                    self.Opositions.append(int(3*y+x))
                return True
                    
    def switchPlayer(self):
        if self.XO == "X":
            self.XO = "O"
        else:
            self.XO = "X"
    
    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].value = ""
        self.Xpositions = []
        self.Opositions = []
        self.XO = "O"
            
    def gameWon(self):
        if self.XO == "X":
            for triple in self.wins:
                if all(i in self.Xpositions for i in triple):
                    return True
        else:
            for triple in self.wins:
                if all(i in self.Opositions for i in triple):
                    return True
        return False
    
    def gameDrawn(self):
        if len(self.Xpositions) + len(self.Opositions) == 9:
            return True
                
class Square:
    def __init__(self, row, col, width, height):
        self.value = ""
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        
    def mark(self,XO):
        if self.value == "":
            self.value = XO
            return True
        
    def draw(self,win):
        gap = self.width / 3
        x = self.col * gap
        y = self.row * gap
        text = mainfont.render(str(self.value),1,(0,0,0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

def redraw_window(win, board, time, Xwins, Owins, Draws):
    win.fill((255,255,255))
    time = timefont.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(time, (540 - 160, 560))
    wins = timefont.render("X:" + str(Xwins) + "  O:" + str(Owins) + "  D:" + str(Draws), 1, (0,0,0))
    win.blit(wins, (40, 560))
    board.draw()

def format_time(secs):
    sec = secs%60
    minute = secs//60
    if sec < 10:
        strsec = "0" + str(sec)
    else:
        strsec = str(sec)
    mat = " " + str(minute) + ":" + strsec
    return mat
    
def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Tic Tac Toe")
    board = Grid(3,3,540,540,win)
    Xwins, Owins, Draws = 0,0,0
    running = True
    start = time.time()
    
    while running:
        play_time = round(time.time()-start)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            if event.type is pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if board.click(pos):
                    if board.gameWon():
                        if board.XO == "X":
                            Xwins += 1
                        else:
                            Owins += 1
                        board.reset()
                    if board.gameDrawn():
                        Draws += 1
                        board.reset()
                    board.switchPlayer()
                
        redraw_window(win,board,play_time,Xwins,Owins,Draws)
        pygame.display.update()
    
main()
pygame.quit()