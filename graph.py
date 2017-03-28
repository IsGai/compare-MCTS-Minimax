import pygame
import draw
import checkWin
import initial

def initialize():
    screen,m,orange = initial.make_screen()
    pygame.display.update()
    running = True
    count = 0
    matrix = [i for i in range(2,66)]
    return running,count,matrix,screen,m,orange

def everything():
    running,count,matrix,screen,m,orange = initialize()
    player_1 = input("Enter your name for player 1:")
    player_2 = input("Enter your name for player 2:")
    print(player_1+" will now go first, you are X")
    print(player_2+" will go second, you are O")
    while running and count < 64:
        a,b,c = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            for i in range(1,65):
                if m["rect"+str(i-1)][1].collidepoint(pygame.mouse.get_pos()): 
                    if pygame.mouse.get_pressed()[0] and not(m["rect"+str(i-1)][2]):
                        count += 1
                        if count%2 == 0:
                            draw.draw_o(screen,i,orange)
                            print("It is now "+player_1+"'s turn:X")
                            m["rect"+str(i-1)][2] = True
                            m["rect"+str(i-1)][0] = 0
                            matrix[i-1] = 0
                        else:
                            y_1,y_2 = draw.find_y(i)
                            draw.draw_left(screen,i,orange,y_1,y_2)
                            print("It is now "+player_2+"'s turn:O")
                            m["rect"+str(i-1)][2] = True
                            m["rect"+str(i-1)][0] = 1
                            matrix[i-1] = 1
                            #print(m["rect"+str(i-1)])
                        if checkWin.check_win(matrix,player_1,player_2):
                            running = False
                        if count == 64:
                            print("Tie")
                    pygame.display.update()


#
# def make_dict():
#     dictionary = {}
#     for i in range(64):
#         dictionary["rect"+str(i)] = i
#     for rect, position in dictionary.items():
#
#
# make_dict()

# class Game(object):
#     def main(self,screen):
#         #sets time per second things will be drawn
#         clock = pygame.time.Clock()
#         image = pygame.image.load("ball")
#         image_x = 0
#         image_y = 0
#         #makes screen gray
#         screen.fill((200,200,200))
#         pygame.screen.update()
#         while 1:
#             #sets it to 10 times per second for drawing
#             clock.tick(10)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     return
#                     #if escape is pressed screen will shut down
#                 if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#                     return
#             #if key is pressed image will move in that direction
#             key =   pygame.key.get_pressed()
#             if key[pygame.K_LEFT]:
#                 image_x -= 10
#             if key[pygame.K_RIGHT]:
#                 image_x += 10
#             if key[pygame.K_UP]:
#                 image_y -= 10
#             if key[pygame.K_DOWN]:
#                 image_y += 10
#             if key[MOUSEBUTTONDOWN]:
#                 image_x += 10
#             #puts an image
#             screen.blit(image, (image_x,image_y))
#             #puts that image onto the screen
#             pygame.display.flip()


# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode((500,500))
    #Game().main(screen)
