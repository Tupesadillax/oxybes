#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import json
import requests
from time import sleep
from datetime import datetime
from database.function import DataBaseFunc
from database.models import Message

url = "https://api.telegram.org/bot" + "5822431321:AAEI0l1TFwCSPTKpW9VhMRCKd2MSGE3Kbb4" + "/"

def create_requets(methodType,methond, **data):
    if data != None:
        r = requests.request(methodType, url + methond, **data)
    else:
        r = requests.request(methodType, url + methond)
    return r.text

def update_info_user(user):
    actualy_subs = [ph for ph in user.purchased_subscriptions if ph.data_end > datetime.now()]
    
    if (len(actualy_subs) == 0):
        user.is_have_subscription = False
        user.subscribe_end = True
        DataBaseFunc.commit()
    
def send_message(user):
    text = "У вас кончилась подписка, пожалуйста, продлите её, чтобы иметь доступ к каналам."
    text_button = "Продлить подписку"
    keyboard = json.dumps(
                           {"inline_keyboard": [[{"text": "Продлить подписку", "callback_data": "subscribe_continue_pay"}], [{"text" : "Связаться с менеджером", "callback_data" : "continue_subs_manager", "url" : "t.me/cyberperu"}]]}
                         )
    
    data = {
            'chat_id' : user.chat_id,
            'text' : text,
            'reply_markup' : keyboard
            }

    answer = create_requets("POST", "sendMessage", data=data)
    message_id = json.loads(answer)['result']["message_id"]
    message = Message(user_id = user.id, message_id=message_id)
    DataBaseFunc.add(message)



def kick_user_from_channel(user, channel):
    is_member = json.loads(create_requets("POST", "getChatMember", data = {'chat_id' : channel.id, 'user_id' : user.id}))['ok']
    
    if(is_member):
        response = create_requets("POST", "kickChatMember", data = {'chat_id' : channel.id, 'user_id' : user.id})

    update_info_user(user)

def send_message_seven(user):
    text = "Добрый день. Ваша подписка на онлайн-курс Юланы Селивановой «Здоровая кожа» заканчивается через неделю. Успейте посмотреть все уроки, которые откладывали на потом. Когда подписка закончится ее можно будет возобновить через бота Telegram."
    data = {
            'chat_id' : user.chat_id,
            'text' : text
            }

    answer = create_requets("POST", "sendMessage", data=data)
    message_id = json.loads(answer)['result']["message_id"]
    message = Message(user_id = user.id, message_id=message_id)
    DataBaseFunc.add(message)
    
all_users = DataBaseFunc.get_users_with_subscribe()
users = [user for user in all_users if user.is_have_subscription]
for user in users:
    for ph in [subs for subs in user.purchased_subscriptions if subs.is_check == False]:
    # for ph in [subs for subs in user.purchased_subscriptions]:
        date = ph.data_end - datetime.now()
        if ((date.days) == 7 and user.is_check_seven_days == False):
            send_message_seven(user)
            user.is_check_seven_days = True
            DataBaseFunc.commit()

        if (ph.data_end > datetime.now()):
            continue
        for channel in ph.courses.channels:
            try:
                kick_user_from_channel(user, channel.channels) 
                ph.is_check = True
                DataBaseFunc.commit()
            except:
                continue
        send_message(user)
