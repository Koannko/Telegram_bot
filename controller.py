# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot
# связывающий модуль, обеспечивающий функционирование
from encodings import utf_8
import model as model
import services

def start():
    bot = []
    with open("bot.txt", "r", encoding = "utf_8") as f:
        while True:
            st = f.readline()
            _st = st.replace(" ","")
            if len(_st) == 0 or _st[0] == "#":
                continue
            bot = st.split()
            break
        
    if len(bot) != 2:
        print("Неверный формат файла bot.txt.")
        print("Bot_user_name Bot_token")
        return
    services.Init(bot)
        
    
def newgame(user_id : int):
    model.newgame(user_id)
    
#Ход пользователя. True - корректный ход
def human_move(user_id, user_input : list ) -> bool:
    return model.human_move(user_id, user_input)
    
#Ход компьютера
def computer_move(user_id):
    model.computer_move(user_id)

def get_board(user_id):
    return model.get_board(user_id)

#проверка на выигрышную ситуацию     
def check_win(user_id) -> bool:
    return model.check_win(user_id)

def check_nomovs(user_id) -> bool:
    return model.check_nomovs(user_id)

#удаляем игру... из словаря
def delete_game(user_id):
    model.delete_game(user_id)

#ПАриглашение ходить ("Вы 0(X). Ваш ход.")    
def your_move(user_id) -> str:
    return model.your_move(user_id)
    