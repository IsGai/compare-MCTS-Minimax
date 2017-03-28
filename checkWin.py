
def who_wins(x,p_1,p_2):
    if x == 0:
        print(p_2+" wins!")
    elif x == 1:
        print(p_1+" wins!")

def four_in_row(matrix,mult,offset,add,iterations,x_or_o):
    for level in range(iterations):
        four_in_row = True
        for i in range(4):
            four_in_row = four_in_row and matrix[(level * mult) + offset + (add * i)] == x_or_o
        if four_in_row:
            return four_in_row
    return four_in_row

def check_win(matrix,p_1,p_2):
    for x_or_o in range(2):
        if four_in_row(matrix,16,0,5,4,x_or_o) or four_in_row(matrix,16,3,3,4,x_or_o) or four_in_row(matrix,1,0,20,4,x_or_o)or four_in_row(matrix,1,12,12,4,x_or_o)or four_in_row(matrix,4,3,15,4,x_or_o)or four_in_row(matrix,1,15,11,1,x_or_o):
            who_wins(x_or_o,p_1,p_2)
            return True
        elif four_in_row(matrix,4,0,17,4,x_or_o)or four_in_row(matrix,1,0,16,16,x_or_o) or four_in_row(matrix,4,0,1,16,x_or_o) or four_in_row(matrix,1,0,21,1,x_or_o) or four_in_row(matrix,1,3,19,1,x_or_o) or four_in_row(matrix,1,12,13,1,x_or_o):
            who_wins(x_or_o,p_1,p_2)
            return True
        for i in range(4):
            if four_in_row(matrix,16,i,4,4,x_or_o):
                who_wins(x_or_o,p_1,p_2)
                return True
    return False

# def enterMatrix(matrix,num,varx_y):
#     matrix.remove(num)
#     if varx_y == "x":
#         matrix.insert(num-2,1)
#     else:
#         matrix.insert(num-2,0)
#     check_win(matrix)

# def enterX(matrix):
#     x = input("Enter which position to place your x: ")
#     is_input_number = True
#     while is_input_number:
#         try:
#             num = int(x)
#             is_input_number = False
#         except ValueError:
#             x = input("Enter a valid integer between 1 and 64: ")
#     while num > 64 or num < 1 or matrix.count(num+1) == 0:
#         if num > 64 or num < 1:
#             print("You did not enter a value between 1 and 64.")
#             num = int(input("Please enter a value between 1 and 64 : "))
#         else:
#             print("That position has a value in it already")
#             num = int(input("Please enter a value between 1 and 64 : "))
#     enterMatrix(matrix,num+1,"x")
#     return num

# def enterO(matrix):
#     x = input("Enter which position to place your o: ")
#     is_input_number = True
#     while is_input_number:
#         try:
#             num = int(x)
#             is_input_number = False
#         except ValueError:
#             x = input("Enter a valid integer between 1 and 64: ")
#     while num > 64 or num < 1 or matrix.count(num+1) == 0:
#         if num > 64 or num < 1:
#             print("You did not enter a value between 1 and 64.")
#             num = int(input("Please enter a value between 1 and 64 : "))
#         else:
#             print("That position has a value in it already")
#             num = int(input("Please enter a value between 1 and 64 : "))
#     enterMatrix(matrix,num+1,"o")
#     return num
