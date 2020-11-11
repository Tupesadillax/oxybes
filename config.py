import os
import json


TOKEN="1185185639:AAE6S_YhsM_FRs7F3xEnsZtqLDxWAbfhPso"
MAIN_ADMIN_ID=454709994
TOKEN_SHOP_YANDEX="390540012:LIVE:12837"

if (os.name == "nt"):
    textsFilename = "texts//text.json"
    texts_but_filename = "texts//text_button.json"
    texts_shedule_filename = "texts//shedule1.txt"
    texts_shedule2_filename = "texts//shedule2.txt"
else:
    textsFilename = "//root//lanamilana_bot_telegram//texts//text.json"
    texts_but_filename = "//root//lanamilana_bot_telegram//texts//text_button.json"
    texts_shedule_filename = "//root//lanamilana_bot_telegram//texts//shedule1.txt"
    texts_shedule2_filename = "//root//lanamilana_bot_telegram//texts//shedule2.txt"

TEXTS = {}

with open(textsFilename, 'r', encoding='utf8') as file:
    TEXTS = json.load(file)


def get_text(user, text):
    return TEXTS[user.lng][text]


TEXTS_BUTTON = {}
with open(texts_but_filename, 'r', encoding='utf8') as file:
    TEXTS_BUTTON = json.load(file)

def get_text_but(user, text):
    return TEXTS_BUTTON[user.lng][text]


