# import telebot


# # API_KEY = "5718246087:AAFm96xbM-mvDgFlBS65vzz6OjkFZagNxYk"

# API_KEY = "5439755812:AAHi4_C4l_PPlUL04N44msFKfVSJO7fIkxU"
# bot = telebot.TeleBot(API_KEY)

# # handle commands, /start
# @bot.message_handler(commands=['start'])
# def handle_command(message):
#     bot.reply_to(message, "Hello, welcome to Telegram Bot!")
    
# # handle all messages, echo response back to users
# @bot.message_handler(func=lambda message: True)
# def handle_all_message(message):
# 	bot.reply_to(message, message.text)

# bot.polling()

import http.client
import json
import os
import random

import requests
from telebot import * 
from telebot import formatting
from flask import Flask, request


API_KEY = "5439755812:AAHi4_C4l_PPlUL04N44msFKfVSJO7fIkxU"
bot = telebot.TeleBot(API_KEY)
bot.delete_webhook()

server = Flask(__name__)


list_of_food = ["MCD", "KFC", "Kopitiam", "Genki", "MAla", "Saizeriya",
                "Korea food", "Japan food", "Western food", "Soup", "Burger King", "Subway"]

list_of_food_joyce = ["Takagi", "Food court", "MCD", "KFC", "Burger King", "Subway",
                      "Bonchon (Lunch deals)", "Pepper Lunch", "Saizeriya", "Yoshinoya", "Poppeyes", "Western", "Mala", "Duck rice", "Chicken rice", "Pasta", "Korean", "Zha Cai Fan", "Ban mian", "Mookata", "Zoeys diner", ]

list_of_food_joyceEx = ["Pizza hut", "Swensens", "Chicken hotpot", "Astons", "Genki", "Ahjumma", "Mookata", "BBQ",
                        "Hotpot", "Bar and drink cocktails ;)", "Din tai fung", "Beauty in a pot"]

funny_text = ["Zuo mo", "Hii", "What you doing", "ByeBye", "ehhhh", "what talking you", "nani", "sayonara", "jiayou", "go away", "don't stress"
                , "hohoo", "tsktsktsk", "smh", "lol", "hahaaaaaaaaaaaa cough**", "gws", "haizzz"]


@bot.message_handler(commands=["random_reply"])
def start(message):
    random.shuffle(funny_text)
    bot.send_message(message.chat.id, funny_text[0])


############################   JOKES  #############################


@bot.message_handler(commands=["joke"])
def joke(message):
    response = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    stringRes = json.loads(response.content)
    if stringRes["type"] == "single":
        bot.send_message(message.chat.id, stringRes["joke"])
    else:
        bot.send_message(message.chat.id, stringRes["setup"])
        bot.send_message(message.chat.id, stringRes["delivery"])


################ FOOD ###########################


@bot.message_handler(commands=["eatwhatah"])
def eatwhatah(message):
    random.shuffle(list_of_food)
    bot.send_message(message.chat.id, list_of_food[0])


@bot.message_handler(commands=["listoffood"])
def eatwhatahlist(message):
    list_of_food.sort()
    food_list = "List of Choices: \n\n"
    for i in list_of_food:
        food_list += i + "\n"

    bot.send_message(message.chat.id, food_list)


####################### FOR JOYCE #########################


@bot.message_handler(commands=["joyce_menu"])
def eatwhatah_joyce(message):
    random.shuffle(list_of_food_joyce)
    bot.send_message(message.chat.id, list_of_food_joyce[0])


@bot.message_handler(commands=["listoffood_joyce"])
def eatwhatahlist_joyce(message):
    list_of_food_joyce.sort()
    food_list = "List of Choices: \n\n"
    for i in list_of_food_joyce:
        food_list += i + "\n"

    bot.send_message(message.chat.id, food_list)


@bot.message_handler(commands=["whenjoycegotmoney"])
def eatwhatah_joyceEx(message):
    random.shuffle(list_of_food_joyceEx)
    bot.send_message(message.chat.id, list_of_food_joyceEx[0])


@bot.message_handler(commands=["whenjoycegotmoney_list"])
def eatwhatahlist_joyceEx(message):
    list_of_food_joyceEx.sort()
    food_list = "List of Choices: \n\n"
    for i in list_of_food_joyceEx:
        food_list += i + "\n"

    bot.send_message(message.chat.id, food_list)


############################## Weather ###############################


conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "7d944c53a7mshb4b428286c343e1p1a9d24jsnd284d9e361b8",
    'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
}


@bot.message_handler(commands=["theweathernow"])
def theweathernow(message):
    split_message = str(message.text).split()
    # print(message)
    # Set Request
    if len(split_message) > 1:
        url_str = "/current.json?q="

        for i in range(1, len(split_message)):
            url_str += split_message[i]
            if i+1 != len(split_message):
                url_str += "%20"

        conn.request("GET", url_str, headers=headers)
    else:
        conn.request("GET", "/current.json?q=Singapore" , headers=headers)

    # Response
    res = conn.getresponse()
    data = res.read().decode('utf-8')

    stringRes = json.loads(data)

    result = "Location: \n"
    for i in stringRes:
        for j, v in stringRes[i].items():
            if j == "name":
                # print(v)
                result += v + "\n\n"
            if j == "last_updated":
                # print(v)
                result += "Last_updated: \n" + v + "\n\n"
            if j == "condition":
                for jj, vv in stringRes[i][j].items():
                    if jj == "text":
                        result += "Condition: " + vv + "\n\n"
            if j == "temp_c":
                result += "Temperature: " + str(v) + "\n\n"

    bot.send_message(message.chat.id, result)
    conn.close()


############################## MUSIC ###############################


@bot.message_handler(commands=["lyricquotes"])
def lyricquotes(message):
    split_message = str(message.text).split()

    url_str = "https://lyric.mackle.im/api?artist=" 
    if len(split_message) > 1:

        for i in range(1, len(split_message)):
            url_str += split_message[i]
            if i+1 != len(split_message):
                url_str += "%20"
        
        response = requests.get(url_str)
        stringRes = json.loads(response.content)
        result = stringRes["info"]["lyrics"] + "\n\n" + "Title: " + stringRes["info"]["title"]

        bot.send_message(message.chat.id, result)
        
    else:
        bot.send_message(message.chat.id, "Please provide artist")


############################## BIBLE ###############################


@bot.message_handler(commands=["bibleverse"])
def bibleverse(message):
    response = requests.get("http://labs.bible.org/api/?passage=random")
    bot.send_message(message.chat.id, response.content, parse_mode="HTML")


############################## ENCOURAGEMENT ###############################


@bot.message_handler(commands=["encouragement"])
def encouragement(message):
    response = requests.get("https://zenquotes.io/api/random")
    stringRes = json.loads(response.content)

    result = ""
    for k, v in stringRes[0].items():
        if k == 'q':
            result += v + "\n\n"
        if k == 'a':
            result += "By: " + v

    bot.send_message(message.chat.id, result)


############################## GAME ###############################


# @bot.message_handler(commands=["cisorpaperstone"])
# def cisorpaperstone(message):

#     standard = ["stone", "paper", "scissor"]
#     obj_list = ["stone", "paper", "scissor"]
#     random.shuffle(obj_list)

#     user_input = str(message.text).split()

#     if len(user_input) > 1:
#         bot.send_message(message.chat.id, obj_list[0])

#         if user_input[1] == obj_list[0]:
#             bot.send_message(message.chat.id, "Tie la")

#         idx = standard.index(user_input[1])
#         idx_bot = standard.index(obj_list[0])
#         last_idx = len(standard) - 1
        
#         if idx == 0 and idx_bot == last_idx:
#             bot.send_message(message.chat.id, "Win liao lor")
#         elif idx_bot == 0 and idx == last_idx:
#             bot.send_message(message.chat.id, "Lose liao lor")
#         elif idx < idx_bot:
#             bot.send_message(message.chat.id, "Lose liao")
#         elif idx > idx_bot:
#             bot.send_message(message.chat.id, "Win liao lor")
#     else:
#         bot.send_message(message.chat.id, "Provide object la")


@bot.message_handler(commands=['cisorpaperstone'])
def cisorpaperstone(message):
    bot.send_message(message.chat.id, text="YOUR MESSAGE HERE", reply_markup=types.ReplyKeyboardRemove())
    print(message.text)


@bot.message_handler(commands=['riddle'])
def riddle(message):
    response = requests.get("https://riddles-api.vercel.app/random")
    stringRes = json.loads(response.content)
    bot.send_message(message.chat.id, stringRes["riddle"])

    bot.send_message(
        message.chat.id,
        formatting.hspoiler(stringRes["answer"]),
        parse_mode='HTML'
    )

bot.polling()

############################## SERVER ###############################


# @server.route('/' + API_KEY, methods=['POST'])
# def getMessage():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return "!", 200


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://musical-octo-eureka.herokuapp.com/' + API_KEY)
#     return "!", 200


# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))