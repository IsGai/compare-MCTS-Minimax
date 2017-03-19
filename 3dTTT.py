import pygame, sys

def draw_vertical(screen,level,grey):
    y_1 = 10 + (170 * level)
    y_2 = 170 + (170 * level)
    for i in range(5):
        x_1 = 100 +(i * 40)
        pygame.draw.line(screen,grey,[x_1,y_1],[x_1,y_2],3)

def draw_horizontal(screen,level,grey):
    x_1 = 100
    x_2 = 260
    for i in range(5):
        y_1 = 10 + (i * 40) +(170 * level)
        pygame.draw.line(screen,grey,[x_1,y_1],[x_2,y_1],3)

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
    x_2 = 260 -(40*(4-offse))
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

def start_pygame(matrix):
    pygame.init()
    screen = pygame.display.set_mode([360,800])
    background = pygame.Surface((360,800))
    gray = (200,200,200)
    grey = (100,100,100)
    background.fill(gray)
    screen.blit(background,(0,0))
    pygame.display.update()
    for i in range(4):
        draw_vertical(screen,i,grey)
        draw_horizontal(screen,i,grey)
    pygame.display.update()
    turn_count = 0
    while check_win(matrix) == False:
        turn_count += 1
        if turn_count%2 == 1:
            draw_value = enterX(matrix)
            draw_x(screen,draw_value,grey)
        else:
            draw_value = enterO(matrix)
            draw_o(screen,draw_value,grey)
        pygame.display.update()
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         #if escape is pressed game is exited
    #         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    #             running = False
#function to make the matrix
def initializeMatrix():
    matrix = []
    for i in range(2,66):
        matrix.append(i)
    return matrix

def four_in_row(matrix,mult,offset,add,iterations,x_or_o):
    for level in range(iterations):
        four_in_row = True
        for i in range(4):
            four_in_row = four_in_row and matrix[(level * mult) + offset + (add * i)] == x_or_o
        if four_in_row:
            return four_in_row
    return four_in_row
#function that enters into the matrix
def check_win(matrix):
    #for level in range(4):
        #verticals for 1 17 33 and 49 -1
    if four_in_row(matrix,16,0,4,4,1)or four_in_row(matrix,16,1,4,4,1)or four_in_row(matrix,16,2,4,4,1)or four_in_row(matrix,16,3,4,4,1)or four_in_row(matrix,16,0,5,4,1) or four_in_row(matrix,16,3,3,4,1):
        return True
        # if matrix[level * 16] == 1 and matrix[level * 16 + 4] == 1 and matrix[level * 16 + 4*2] == 1 and matrix[level * 16 + 4*3] == 1:
        #     return True
    # elif matrix[level * 16 + 1] == 1 and matrix[level * 16 + 1 + 4] == 1 and matrix[level * 16 + 1 + 4*2] == 1 and matrix[level * 16 + 1 + 4*3] == 1:
    #         return True
    # elif matrix[level * 16 + 2] == 1 and matrix[level * 16 + 2 + 4] == 1 and matrix[level * 16 + 2 + 4*2] == 1 and matrix[level * 16 + 2 + 4*3] == 1:
    #         return True
    # elif matrix[level * 16 + 3] == 1 and matrix[level * 16 + 3 + 4] == 1 and matrix[level * 16 + 3 + 4*2] == 1 and matrix[level * 16 + 3 + 4*3] == 1:
    #         return True
    # elif matrix[level * 16] == 1 and matrix[level * 16 + 5] == 1 and matrix[level * 16 + 5*2] == 1 and matrix[level * 16 + 5*3] == 1:
    #         return True
    # elif matrix[level * 16 + 3] == 1 and matrix[level * 16 + 3 + 3] == 1 and matrix[level * 16 + 3 + 3*2] == 1 and matrix[level * 16 + 3 + 3*3] == 1:
    #         return True
    elif four_in_row(matrix,1,0,20,4,1)or four_in_row(matrix,1,12,12,4,1)or four_in_row(matrix,4,3,15,4,1)or four_in_row(matrix,4,0,17,4,1)or four_in_row(matrix,1,0,16,16,1) or four_in_row(matrix,4,0,1,16,1):
        return True
    elif four_in_row(matrix,1,0,21,1,1) or four_in_row(matrix,1,3,19,1,1) or four_in_row(matrix,1,12,13,1,1) or four_in_row(matrix,1,15,11,1,1):
        return True
    elif four_in_row(matrix,16,0,4,4,0)or four_in_row(matrix,16,1,4,4,0)or four_in_row(matrix,16,2,4,4,0)or four_in_row(matrix,16,3,4,4,0)or four_in_row(matrix,16,0,5,4,0) or four_in_row(matrix,16,3,3,4,0):
        return True
    elif four_in_row(matrix,1,0,20,4,0)or four_in_row(matrix,1,12,12,4,0)or four_in_row(matrix,4,3,15,4,0)or four_in_row(matrix,4,0,17,4,0)or four_in_row(matrix,1,0,16,16,0) or four_in_row(matrix,4,0,1,16,0):
        return True
    elif four_in_row(matrix,1,0,21,1,0) or four_in_row(matrix,1,3,19,1,0) or four_in_row(matrix,1,12,13,1,0) or four_in_row(matrix,1,15,11,1,0):
        return True
    #         return True
    # elif matrix[level + 12] == 1 and matrix[level + 12 + 12] == 1 and matrix[level + 12 + 12*2] == 1 and matrix[level + 12 + 12*3] == 1:
    #         return True
    # elif matrix[level * 4 + 3] == 1 and matrix[level * 4 + 3 + 15] == 1 and matrix[level * 4 + 3 + 15*2] == 1 and matrix[level * 4 + 3 + 15*3] == 1:
    #         return True
    # elif matrix[level * 4] == 1 and matrix[level * 4 + 17] == 1 and matrix[level * 4 + 17*2] == 1 and matrix[level * 4 + 17*2] == 1:
    #         return True
    # for down in range(16):
    #     if matrix[down] == 1 and matrix[down + 16] == 1 and matrix[down + 16*2] == 1 and matrix[down + 16*3] == 1:
    #         return True
    # for row in range(16):
    #     if matrix[row * 4] == 1 and matrix[row * 4 + 1] == 1 and matrix[row * 4 + 2] == 1 and matrix[row * 4 + 3] == 1:
    #         return True
    # row = 0
    # if matrix[row] == 1 and matrix[row + 21] == 1 and matrix[row + 21*2] == 1 and matrix[row + 21*3] == 1:
    #     return True
    # elif matrix[row + 3] == 1 and matrix[row + 3 + 19] == 1 and matrix[row + 3 + 19*2] == 1 and matrix[row + 3 + 19*3] == 1:
    #     return True
    # elif matrix[row + 12] == 1 and matrix[row + 12 + 13] == 1 and matrix[row + 12 + 13*2] == 1 and matrix[row + 12 + 13*3] == 1:
    #     return True
    # elif matrix[row + 15] == 1 and matrix[row + 15 + 11] == 1 and matrix[row + 15 + 11*2] == 1 and matrix[row + 15 + 11*3] == 1:
    #     return True
    return False

def enterMatrix(matrix,num,varx_y):
    matrix.remove(num)
    if varx_y == "x":
        matrix.insert(num-2,1)
    else:
        matrix.insert(num-2,0)
        #function to check if win
    check_win(matrix)

def enterX(matrix):
    x = input("Enter which position to place your x: ")
    is_input_number = True
    while is_input_number:
        try:
            num = int(x)
            is_input_number = False
        except ValueError:
            x = input("Enter a valid integer between 1 and 64: ")
    while num > 64 or num < 1 or matrix.count(num+1) == 0:
        if num > 64 or num < 1:
            print("You did not enter a value between 1 and 64.")
            num = int(input("Please enter a value between 1 and 64 : "))
        else:
            print("That position has a value in it already")
            num = int(input("Please enter a value between 1 and 64 : "))
    enterMatrix(matrix,num+1,"x")
    return num

def enterO(matrix):
    x = input("Enter which position to place your o: ")
    is_input_number = True
    while is_input_number:
        try:
            num = int(x)
            is_input_number = False
        except ValueError:
            x = input("Enter a valid integer between 1 and 64: ")
    while num > 64 or num < 1 or matrix.count(num+1) == 0:
        if num > 64 or num < 1:
            print("You did not enter a value between 1 and 64.")
            num = int(input("Please enter a value between 1 and 64 : "))
        else:
            print("That position has a value in it already")
            num = int(input("Please enter a value between 1 and 64 : "))
    enterMatrix(matrix,num+1,"o")
    return num

def main():
    matrix = initializeMatrix()
    start_pygame(matrix)
    #while check_win(matrix) == False:
    #    enterX(matrix)
        #print(matrix)
    print("Four in a row!")


main()
