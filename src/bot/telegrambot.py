# Example code for telegrambot.py module
import json

import collections
import collections.abc
import copy

import apiai as apiai
import requests

from bot.models import SlackNotice
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyMarkup
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater
from django_telegrambot.apps import DjangoTelegramBot
from bot.dialog import *
from bot.items import *
import logging

logger = logging.getLogger(__name__)

# состояние разговоров
handlers = {}
last_message_ids = {}


# Получить состояние разговора по номеру чата
# Если разговора еще не было, то создаем новый
def get_handler(chat_id):
    if chat_id not in handlers:
        result = None
        return True, result
    return False, handlers[chat_id]


def handle_message(bot, update, **kwargs):
    print("Received", update.message)
    chat_id = update.message.chat_id
    generator = hello('')
    if update.message.text == "/start":
        handlers.pop(chat_id, None)

    if update.message.text == "/ticket":
        handlers.pop(chat_id, None)
        generator = hello('')
    apply_handler(bot, chat_id, generator, update.message)


def apply_handler(bot, chat_id, generator,  message=None):
    just_started, handler = get_handler(chat_id)
    if just_started:
        handler = handlers[chat_id] = generator
        answer = next(handler)
    else:
        try:
            print(message.text)
            answer = handler.send(message)
        except StopIteration as e:
            del handlers[chat_id]
            return False
        except GeneratorExit as e:
            del handlers[chat_id]
            answer = str(e)
    send_answer(bot, chat_id, answer)


def send_answer(bot, chat_id, answer):
    print("Sending answer %r to %s" % (answer, chat_id))
    if isinstance(answer, collections.abc.Iterable) and not isinstance(answer, str):
        # мы получили несколько объектов -- сперва каждый надо обработать
        answer = list(map(_convert_answer_part, answer))
    else:
        # мы получили один объект -- сводим к более общей задаче
        answer = [_convert_answer_part(answer)]
    # перед тем, как отправить очередное сообщение, идём вперёд в поисках
    # «довесков» -- клавиатуры там или в перспективе ещё чего-нибудь
    current_message = last_message = None
    for part in answer:
        if isinstance(part, Message):
            if current_message is not None:
                # сообщение, которое мы встретили раньше, пора бы отправить.
                # поскольку не все объекты исчерпаны, пусть это сообщение
                # не вызывает звоночек (если не указано обратное)
                current_message = copy.deepcopy(current_message)
                current_message.options.setdefault("disable_notification", True)
                _send_or_edit(bot, chat_id, current_message)
            current_message = part
        if isinstance(part, ReplyMarkup):
            # ага, а вот и довесок! добавляем текущему сообщению.
            # нет сообщения -- ну извините, это ошибка.
            current_message.options["reply_markup"] = part
    # надо не забыть отправить последнее встреченное сообщение.
    if current_message is not None:
        _send_or_edit(bot, chat_id, current_message)


def _send_or_edit(bot, chat_id, message):
    if isinstance(message, EditLast):
        bot.editMessageText(text=message.text, chat_id=chat_id, message_id=last_message_ids[chat_id],
                            **message.options)
    else:
        print("Sending message: %r" % message.text)
        last_message_ids[chat_id] = bot.sendMessage(chat_id=chat_id, text=message.text, **message.options)


def _convert_answer_part(answer_part):
    if isinstance(answer_part, str):
        return Message(answer_part)
    if isinstance(answer_part, (collections.abc.Iterable, Keyboard)):
        # клавиатура?
        resize_keyboard = False
        one_time_keyboard = True

        if isinstance(answer_part, collections.abc.Iterable):
            answer_part = list(answer_part)
        else:
            one_time_keyboard = answer_part.one_time_keyboard
            resize_keyboard = answer_part.resize_keyboard
            answer_part = answer_part.markup

        if isinstance(answer_part[0], str):
            # она! оформляем как горизонтальный ряд кнопок.
            # кстати, все наши клавиатуры одноразовые -- нам пока хватит.
            return ReplyKeyboardMarkup([answer_part], one_time_keyboard=one_time_keyboard,
                                       resize_keyboard=resize_keyboard)
        elif isinstance(answer_part[0], collections.abc.Iterable):
            # двумерная клавиатура?
            answer_part = list(map(list, answer_part))
            if isinstance(answer_part[0][0], str):
                # она!
                return ReplyKeyboardMarkup(answer_part, one_time_keyboard=one_time_keyboard,
                                           resize_keyboard=resize_keyboard)
    if isinstance(answer_part, Inline):
        return answer_part.convert()
    return answer_part


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def smalltalk(bot, update):
    chat_id = update.message.chat_id
    just_started, handler = get_handler(chat_id)
    if just_started:
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
    else:
        handle_message(bot, update)


def help(bot, update):
    text = 'Поддерживаемые команды:' + '\n' + '\n' + \
           '/help - Список доступных команд бота' + '\n' + \
           '/ticket [текст заявки]- Отправить заявку в службу техподдержки "Сибинтек"' + '\n' + \
           'Например: /ticket не работает принтер на АЗК 100' + '\n' + \
           '/weather - Прогноз погоды в Иркутске' + '\n' + \
           '/citate - Случайная цитата с сайта forismatic.com'

    bot.sendMessage(update.message.chat_id, text=text)


def order(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    just_started, handler = get_handler(chat_id)
    if just_started:
        answer = next(handler)
    else:
        try:
            answer = handler.send(message)
        except StopIteration:
            answer = 'Кончились вопросы'
            pass
            # del handlers[chat_id]
    bot.sendMessage(update.message.chat_id, text=answer)
    # noticies = SlackNotice.objects.filter(type=SlackNotice.TBOT_ORDER)
    # try:
    #     text = update.message.text[update.message.text.index(' '):].strip()
    #     reply_text = 'Заявка отправлена!'
    #     attachments = [
    #         {
    #             'fields': [
    #                 {
    #                     "title": text,
    #                     "short": False,
    #                 },
    #             ],
    #         },
    #     ]
    #     for notice in noticies:
    #         notice.send('Новая заявка:', attachments)
    # except:
    #     reply_text = 'Не правильно введена команда!\nПример команды: \n /ticket на АЗК 100 не работает принтер'
    #
    # bot.sendMessage(update.message.chat_id, text=reply_text)


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
    dp.add_handler(MessageHandler(Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.private, smalltalk))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    # message_handler =
    # inline_query_handler = InlineQueryHandler(self.handle_inline_query)

    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("ticket", order))
    # dp.add_handler(CommandHandler("weather", weather))
    # dp.add_handler(CommandHandler("citate", citate))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, text))

    # log all errors
    dp.add_error_handler(error)
