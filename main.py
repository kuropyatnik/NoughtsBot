import telebot, skynet
import markups as m
import sys
from telebot import types
token = "<my_token>"
bot = telebot.TeleBot(token)
print(sys.version)
arrow = u'\U000023EC'
#class with fields, that must be unique for each user
class User:
    markup = types.InlineKeyboardMarkup()
    text = ""
    def __init__(self, id, field, ai, human, counter, level):
        self.id = id
        self.field = field
        self.ai = ai
        self.human = human
        self.counter = counter
        self.level = level
#dict for working with multiple users
users = {}
#strings for messages
startText = "Hello, i am tic tac toe bot. Bet that i will beat you :-)"
helpText = "/start - start working with bot;\n /new_game - start a new game;\n /help - list of all commands;\n"
levelText = "Choose difficulty level:"
sideText = "Choose your side"
aiWinText = "Oh, i win! How about one more game?"
humanWinText = "You win! How about one more game?"
drawText = "Looks like we are equal! How about one more game?"
byeText = "Looking forward to play again!"
#Clear all values for concrete user
def clear(id):
    field = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    ai = ""
    human = ""
    level = 0
    counter = 0
    currUser = User(id, field, ai, human, counter, level)
    users[currUser.id] = currUser
#Make move for ai
def ai_move(field, ai, level, human, counter):
    # Now AI move
    if (level == 1):
        skynet.jun(field, ai)
    elif (level == 2):
        lucky = skynet.random.choice([1, 2])
        if (lucky == 1):
            skynet.jun(field, ai)
        else:
            skynet.sen(field, ai,human, counter)
    elif (level == 3):
        skynet.sen(field, ai, human, counter)
#Input data about current message
def prev_mess(id, text, markup):
    users[id].text = text
    users[id].markup = markup
#Handler for start working
@bot.message_handler(commands=["start"])
def start(message):
    cid = message.chat.id
    if (len(users) > 0 and users[cid].level > 0):
        bot.edit_message_text(text=arrow, chat_id=cid, message_id=message.message_id - 1)
        bot.send_message(cid, text=users[cid].text, reply_markup=users[cid].markup)
    else:
        clear(cid)
        prev_mess(cid, startText, types.InlineKeyboardMarkup())
        bot.send_message(message.chat.id, startText)
#Handler for list of all existing commands
@bot.message_handler(commands=["help"])
def help(message):
    cid = message.chat.id
    if (users[cid].level > 0):
        bot.edit_message_text(text=arrow, chat_id=cid, message_id=message.message_id - 1)
        bot.send_message(cid, text=users[cid].text, reply_markup=users[cid].markup)
    else:
        prev_mess(cid, helpText, types.InlineKeyboardMarkup())
        bot.send_message(message.chat.id, helpText)
        print(message.text)
#Handler for start a new game
@bot.message_handler(commands=["new_game"])
def new_game(message):
    cid = message.chat.id
    if (users[cid].level > 0):
        bot.edit_message_text(text=arrow, chat_id=cid, message_id=message.message_id - 1)
        bot.send_message(cid, text=users[cid].text, reply_markup=users[cid].markup)
    else:
        clear(cid)
        bot.send_message(users[cid].id, text=levelText, reply_markup=m.levelMarkup)
        prev_mess(cid, levelText, m.levelMarkup)
        users[cid].level = 100
#Handler for any non-readeble text
@bot.message_handler(content_types=["text"])
def any_msg(message):
    #We need to resend prev bot message and alert user, that message isn`t recognized
    cid = message.chat.id
    bot.edit_message_text(text=arrow, chat_id=cid, message_id=message.message_id - 1)
    bot.send_message(cid, text=users[cid].text, reply_markup=users[cid].markup)
#Handler for all callback btns
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        chatID = call.message.chat.id
        if (call.data[0] == "l"):#Level modification
            users[chatID].level = int(call.data[1:])
            bot.edit_message_text(text=sideText, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=m.sideMarkup)
            prev_mess(chatID, sideText, m.sideMarkup)
        elif (call.data[0] == "s"):#First field creating
            users[chatID].human = call.data[1:]
            if (users[chatID].human == "x"):
                users[chatID].ai = "0"
            elif (users[chatID].human == "0"):
                users[chatID].ai = "x"
                ai_move(users[chatID].field, users[chatID].ai, users[chatID].level, users[chatID].human, users[chatID].counter)
                users[chatID].counter += 1
            # Field drawing - 3x3 callback buttons
            fieldMarkup = m.draw_field(users[chatID].field)
            bot.edit_message_text(text="You will play as " + users[chatID].human + ", get ready!",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=fieldMarkup)
            prev_mess(chatID, "You will play as " + users[chatID].human + ", get ready!", fieldMarkup)
        elif (call.data[0] == "i"):
            crds = str.split(call.data[1:], ';')
            if (users[chatID].field[int(crds[0])][int(crds[1])] != '-'):
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Field isn`t empty!")
                print(call.data)
            else:
                # Human move
                users[chatID].field[int(crds[0])][int(crds[1])] = users[chatID].human
                users[chatID].counter += 1
                res = skynet.is_win(users[chatID].field)
                if (res[0] == True):
                    text, resultMarkup =  m.result_game(users[chatID].field, humanWinText)
                    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                          message_id=call.message.message_id, reply_markup=resultMarkup)
                    prev_mess(chatID, text, resultMarkup)
                elif (users[chatID].counter == 9):
                    text, resultMarkup = m.result_game(users[chatID].field, drawText)
                    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                          message_id=call.message.message_id, reply_markup=resultMarkup)
                    prev_mess(chatID, text, resultMarkup)
                else:
                    ai_move(users[chatID].field, users[chatID].ai, users[chatID].level, users[chatID].human,
                            users[chatID].counter)
                    users[chatID].counter += 1
                    res = skynet.is_win(users[chatID].field)
                    if (res[0] == True):
                        text, resultMarkup = m.result_game(users[chatID].field, aiWinText)
                        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=resultMarkup)
                        prev_mess(chatID, text, resultMarkup)
                    elif (users[chatID].counter == 9):
                        text, resultMarkup = m.result_game(users[chatID].field, drawText)
                        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=resultMarkup)
                        prev_mess(chatID, text, resultMarkup)
                    else:
                        # Отрисовка пользователю
                        fieldMarkup = m.draw_field(users[chatID].field)
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=fieldMarkup)
                        prev_mess(chatID, users[chatID].text, fieldMarkup)
                        print(call.data)
        elif (call.data[0] == "n"):
            answer = call.data[1:]
            if (answer == "y"):
                clear(chatID)
                bot.edit_message_text(text=levelText, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id, reply_markup=m.levelMarkup)
                prev_mess(chatID, levelText, m.levelMarkup)
            else:
                bot.edit_message_text(text=byeText, chat_id=call.message.chat.id, message_id=call.message.message_id)
                prev_mess(chatID, byeText, types.InlineKeyboardMarkup())
                users[chatID].level = 0
if __name__ == "__main__":
    bot.polling(none_stop=True)