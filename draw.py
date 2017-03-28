import pygame

def offset(number):
    offset = number%4
    if number%4 == 0 :
        offset = 4
    return offset

def draw_left(screen,number,grey,y_1,y_2):
    offse = offset(number)
    x_1 = 60 +(40*offse)
    x_2 = 40 + x_1
    pygame.draw.line(screen,grey,[x_1,y_1],[x_2,y_2],3)
    draw_right(screen,number,grey,y_1,y_2)

def draw_right(screen,number,grey,y_1,y_2):
    offse = offset(number)
    x_2 = 259 -(40*(4-offse))
    x_1 = x_2 - 40
    pygame.draw.line(screen,grey,[x_2,y_1],[x_1,y_2],3)

def find_y(number):
    tracker = (number-1) // 4
    level_tracker = (number-1) // 16
    y_1 = 10 + (40*tracker) + (10*level_tracker)
    y_2 = y_1 + 40
    return y_1,y_2

def draw_x(screen,number,grey):
    y_1,y_2 = find_y(number)
    draw_left(screen,number,grey,y_1,y_2)

def draw_o(screen,number,red):
    y_1,y_2 = find_y(number)
    y_1 += 20
    offse = offset(number)
    x_1 = 60 +(40*offse) + 20
    pygame.draw.circle(screen,red,(x_1,y_1),20,3)
