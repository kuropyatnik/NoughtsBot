#All markups for callback buttons
from telebot import types
x = u'\U0000274C'
o = u'\U00002B55'
e = u'\U00002B1C'
#Level
levelMarkup = types.InlineKeyboardMarkup()
clb1 = types.InlineKeyboardButton(text="Junior", callback_data="l1")
clb2 = types.InlineKeyboardButton(text="Middle", callback_data="l2")
clb3 = types.InlineKeyboardButton(text="Senior", callback_data="l3")
levelMarkup.add(clb1, clb2, clb3)
#Side
sideMarkup = types.InlineKeyboardMarkup()
clb1 = types.InlineKeyboardButton(text=x, callback_data="sx")
clb2 = types.InlineKeyboardButton(text=o, callback_data="s0")
sideMarkup.add(clb1, clb2)
#Field
def draw_field(f):
    # Отрисовка пользователю
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(f)):
        btns = []
        for j in range(len(f[i])):
            index = str(i) + ";" + str(j)
            if (f[i][j] == '-'):
                callback_button = types.InlineKeyboardButton(text=e, callback_data="i" + index)
            elif (f[i][j] == 'x'):
                callback_button = types.InlineKeyboardButton(text=x, callback_data="i" + index)
            else:
                callback_button = types.InlineKeyboardButton(text=o, callback_data="i" + index)
            btns.append(callback_button)
        keyboard.add(btns[0], btns[1], btns[2])
    return keyboard
#Result
def result_game(f, res_text):
    keyboard = types.InlineKeyboardMarkup()
    clb1 = types.InlineKeyboardButton(text="Hell yeah!", callback_data="ny")
    clb2 = types.InlineKeyboardButton(text="No, I`m scared", callback_data="nn")
    keyboard.add(clb1, clb2)
    text = ""
    for i in range(len(f)):
        for j in range(len(f[i])):
            if (f[i][j] == '-'):
                text += e + " "
            elif (f[i][j] == 'x'):
                text += x + " "
            else:
                text += o + " "
        text += "\n"
    text += res_text
    return text, keyboard