# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot
# 
import random

""" в словаре boards храним кофигурацию игровых полей
 {id(int) : [[y][x], sign : int ]} sign == 1 -'X' sign == 2 - '0'
"""
boards = {}

def newgame(user_id : int):
    '''
    Новая игра для игрока [user_id]
    случайно выбираем кто человек '0' или 'X' (первый ход -  "X")
    sign == 1 -'X' sign == 2 - '0' 
    '''
    global boards
    sign = random.randint(0, 10) % 2 + 1   
    boards[user_id] = [[[0 for x in range(0, 3)] for y in range(0, 3)], sign]
    
    if(sign == 2):
        computer_move(user_id)
    


def computer_move(user_id : int):
    """ Ход компьютера  """
    global boards    
    if boards[user_id][1] == 1:
        sign = 2
    else:
        sign = 1
    board = boards[user_id][0]
    while True:
        x =  random.randint(0, 2)
        y =  random.randint(0, 2)
        if board[y][x] == 0:
            board[y][x] = sign
            return



def get_board(user_id : int) -> str:
    """ строка для отрисовки игровой доски  """
    global boards    
    board = boards[user_id][0]
    st = ""
    for y in board:
        for it in y:
            if it == 0:
                st += "|  "
            elif it == 1:
                st += "|X"
            else:
                st += "|0"
        st += "|\n"
    return st

                
    
def check_win(user_id : int) -> bool:
    """    Проверка выигрышной ситуации    """
    global boards    
    board = boards[user_id][0]    
    for i in range(0, 3): #поле небольшое 3 х 3 поэтому делаем проверку "в лоб"
        if board[i][0] == board[i][1] == board[i][2] != 0  or board[0][i] == board[1][i] == board[2][i] != 0:
            return True
    if board[0][0] == board[1][1] == board[2][2] != 0 or board[0][2] == board[1][1] == board[2][0] != 0:
        return True
    return False

def check_nomovs(user_id : int) -> bool:
    global boards    
    board = boards[user_id][0]
    for y in board:
        if 0 in y:
            return False
    return True


    
def human_move(user_id : int, inp : list) -> bool:
    """  Ход человека (x  y) True - если ход верный   """
    global boards    
    board = boards[user_id][0]
    sign = boards[user_id][1]        
    while True:
        if len(inp) == 2:
            if board[int(inp[1])] [int(inp[0])] == 0:
                board[int(inp[1])] [int(inp[0])] = sign
                return True
        return False # Неверный ввод пользователя "Ошибка! Попробуйте снова..."
        

    
def delete_game(user_id):
    """   Удаление игры [user_id] из словаря    """
    global boards
    boards.pop(user_id, None)

