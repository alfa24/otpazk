# Example code for telegrambot.py module
import json

import apiai as apiai
import requests

from bot.models import SlackNotice
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

import logging

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def smalltalk(bot, update):
    request = apiai.ApiAI('4e48db01a8eb487797d0eed3f1bdd370').text_request()  # small talk
    # request = apiai.ApiAI('7377522fa62f481bb8af3058ed0ba6e6').text_request()  # tech support
    # request = apiai.ApiAI('f920d4b6978c4d5481fd19b82aa989d4').text_request()  # погода
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


def help(bot, update):
    text = 'Поддерживаемые команды:' + '\n' + '\n' + \
           '/help - Список доступных команд бота' + '\n' + \
           '/ticket [текст заявки]- Отправить заявку в службу техподдержки "Сибинтек"' + '\n' + \
           'Например: /ticket не работает принтер на АЗК 100' + '\n' + \
           '/weather - Прогноз погоды в Иркутске' + '\n' + \
           '/citate - Случайная цитата с сайта forismatic.com'

    bot.sendMessage(update.message.chat_id, text=text)


def order(bot, update):
    noticies = SlackNotice.objects.filter(type=SlackNotice.TBOT_ORDER)
    try:
        text = update.message.text[update.message.text.index(' '):].strip()
        reply_text = 'Заявка отправлена!'
        attachments = [
            {
                'fields': [
                    {
                        "title": text,
                        "short": False,
                    },
                ],
            },
        ]
        for notice in noticies:
            notice.send('Новая заявка:', attachments)
    except:
        reply_text = 'Не правильно введена команда!\nПример команды: \n "/ticket на АЗК 100 не работает принтер"'

    bot.sendMessage(update.message.chat_id, text=reply_text)


def text(bot, update):
    if update.message.text.startswith("@otpazk_bot"):
        smalltalk(bot, update)
    else:
        noticies = SlackNotice.objects.filter(type=SlackNotice.TBOT_ALL)
        attachments = [
        ]
        text = ''
        first_name = str(update.effective_user['first_name'])
        last_name = str(update.effective_user['last_name'])
        if first_name:
            text += first_name
        if last_name:
            text += ' ' + last_name
        print(update.effective_user['first_name'])
        print(update.effective_user['last_name'])
        text += ': ' + str(update.message.text)
        for notice in noticies:
            notice.send(text, attachments)


def photo(bot, update):
    noticies = SlackNotice.objects.filter(type=SlackNotice.TBOT_ALL)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    attachments = [
        {
            "image_url": photo_file['file_path'],
        }
    ]
    text = str(update.effective_user['first_name']) + ' ' + str(update.effective_user['username'])

    for notice in noticies:
        notice.send(text, attachments)


def weather(bot, update):
    s_city = "Irkutsk,RU"
    city_id = 2023469
    appid = "2cf741b207964a4fd3fe7c672f6e260a"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        text = ''
        for i in data['list']:
            if '12:00:00' in i['dt_txt']:
                # print(i['dt_txt'][:10], '{0:+8.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
                text += str(i['dt_txt'][:10]) + \
                        '{0:+8.0f}   '.format(i['main']['temp']) + \
                        str(i['weather'][0]['description']) + \
                        '\n'
        bot.sendMessage(update.message.chat_id, text=text)
    except Exception as e:
        print("Exception (forecast):", e)
        pass


def citate(bot, update):
    res = requests.get("http://api.forismatic.com/api/1.0/",
                       params={'method': 'getQuote', 'key': '457653', 'lang': 'ru', 'format': 'json'})
    data = res.json()
    author = data['quoteAuthor']
    if len(author) == 0:
        author = 'Неизвестный'
    text = 'Случайная цитата: \n' + \
           '"' + data['quoteText'] + \
           '"\n' + '\n' + \
           'Автор: ' + author + '\n'
    bot.sendMessage(update.message.chat_id, text=text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ticket", order))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("citate", citate))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.private, smalltalk))
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(MessageHandler(Filters.photo, photo))

    # log all errors
    dp.add_error_handler(error)
