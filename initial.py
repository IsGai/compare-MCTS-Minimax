import draw
import pygame

def draw_rect(screen,red,background):
    m = {}
    for number in range(1,65):
        a = "rect"
        g = a + str(number-1)
        offse = draw.offset(number)
        x_1 = 60 +(40*offse)
        y_1,y_2 = draw.find_y(number)
        # pygame.draw.rect(g,red,300,2)
        g = pygame.draw.rect(background,red,(x_1,y_1,39,39))
        m[a+str(number-1)] = [number + 1,g,False]
        screen.blit(background,(0,0))
    return m
#has to be run before anything
def make_screen():
    pygame.init()
    screen = pygame.display.set_mode((360,800))
    background = pygame.Surface((360,800))
    gray = (255,255,255)
    grey = (200,200,200)
    red = (00,0,100)
    orange = (255,140,0)
    background.fill(grey)
    screen.blit(background,(0,0))
    return screen,draw_rect(screen,red,background),orange

def initialize():
    screen,m,orange = make_screen()
    pygame.display.update()
    running = True
    count = 0
    matrix = [i for i in range(2,66)]
    return running,count,matrix
