# GBTeam2
# Групповая работа по созданию игры "крестики - нолики" с использованием telegram - bot

# /start
# /help - выводит список и описание команд
# /move 0 1          x[0..2] y[0..2]
# /draw - отрисовка доски

import controller

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler



def Init(bot : list):
    token = bot[1]
    app = ApplicationBuilder().token(token).build()
        #'5665588710:AAF41tF61xNX7XKc-vmkvwfKswBbeGW62sw' #@kfh1567_bot

    start_handler = CommandHandler('start', start)
    move_handler = CommandHandler('move', move)
    draw_handler = CommandHandler('draw', draw)
    help_handler = CommandHandler('help', help)
    app.add_handler(move_handler)
    app.add_handler(draw_handler)
    app.add_handler(help_handler)
    app.add_handler(start_handler)

    print(f"\nТелеграм-бот: {bot[0]} запущен")
    app.run_polling()




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    controller.newgame(user_id)
    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id), parse_mode="html")


async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = context.args#[:-2]
    if not controller.human_move(user_id, user_input):
        st = """<b>Неверное значение!</b>
        Поле занято или не существует. Чтобы продолжить введите '[номер столбца (0..2)] [номер строки (0..2)]'.
        Например, /move 1 2        
        """
        await context.bot.send_message(chat_id=update.effective_user.id, text = st, parse_mode="html")
        return

    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id), parse_mode="html")
    if not await check(user_id, context, person = 1):
        return

    controller.computer_move(user_id)
    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id), parse_mode="html")    
    if not await check(user_id, context, person = 2):
        return


async def check(user_id : int, context, person : int):
    if controller.check_win(user_id):
        if person == 1:
            await context.bot.send_message(chat_id = user_id, text="Поздравляю! Вы выиграли! Сыграем еще раз? /start", parse_mode="html")
        else:
            await context.bot.send_message(chat_id = user_id, text="Вы проиграли. Сыграем еще раз? /start", parse_mode="html")
        controller.delete_game(user_id)
        return 0

    if controller.check_nomovs(user_id):
        await context.bot.send_message(chat_id = user_id, text="Ничья! Сыграем еще раз? /start", parse_mode="html")
        controller.delete_game(user_id)
        return 0
    return 1


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=update.effective_user.id, text=controller.get_board(user_id)+'\nВаш ход', parse_mode="html")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    st = """<b>Правила игры</b>
Игроки по очереди ставят на свободные клетки поля 3×3 знаки. Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или диагонали, выигрывает.
Первый ход делает игрок, ставящий крестики.
<b>/start</b> - начать новую игру
<b>/help</b> - помощь по игре
<b>/draw</b> - показать доску
<b>/move</b> - сделать ход.<b>Формат ввода</b>: 
    /move [номер столбца (0..2)] [номер строки (0..2)]
    Например: /move 1 2"""
    await context.bot.send_message(chat_id=update.effective_user.id, text = st, parse_mode="html")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
