# -*- coding: utf-8 -*-
from bot.models import SlackNotice
from main.models import Person, EmployeesAZK, Azs


def get_person(user_id):
    try:
        person = Person.objects.get(telegram_id=user_id)
        answer = ''
    except:
        person, answer = yield from hello(user_id)

    if not person.is_active:
        answer += "\nПользователь не авторизован. Попросите модератора вас авторизовать.\n" + \
                  "Пришлите ему ваш telegram ID: %s\n" % user_id
        hr = Person.objects.filter(hr=True)
        if hr.count() > 0:
            answer += "\nСпиcок модераторов:\n"
            for person_hr in hr:
                answer += str(person_hr) + "\n"

    return person, answer


def get_person_info(person):
    answer = "Нет информации."
    result = False

    if person:
        # инфа о физлице
        answer = "\n===Информация о Вас=== \n" \
                 "Ваш telegram ID: %s \n" \
                 "ФИО: %s \n" \
                 "Телефон: %s \n" \
                 "Место работы: %s \n\n" % \
                 (person.telegram_id,
                  person.name,
                  person.phone,
                  person.description)

        # инфа как о сотруднике
        empls = EmployeesAZK.objects.filter(person=person)
        for empl in empls:
            answer += "Объект: %s\n" \
                      "Должность: %s\n" \
                      "Статус учетной записи TradeHouse: %s\n" \
                      "Логин TradeHouse: %s\n" \
                      "Пароль TradeHouse: %s\n\n" % \
                      (empl.azk,
                       empl.position,
                       empl.status,
                       empl.login,
                       empl.password)
        result = True

    return result, answer


def hello(user_id):
    answer = yield "Здравствуйте! Мы еще не знакомы! \n" \
                   "Я Агент техподдержки Сибинтек.\n" \
                   "А Вы? \n" \
                   "Напишите свое полное ФИО."
    name = str(answer.text)
    answer = yield "Приятно познакомиться, %s.\n" \
                   "Если вы работаете на АЗК/АЗС, то напишите полный номер АЗК?\n" \
                   "Например: 055\n" \
                   "\nЕсли в другом месте, то название вашей компании." % name
    workname = answer.text.lower()
    answer = yield "Напишите ваш номер телефона.\n" \
                   "Например: 89025566777"
    phone = answer.text

    saved = yield from ask_yes_or_no("Сохраняем информацию о Вас?")
    if saved:

        if Person.objects.filter(telegram_id=user_id).count() > 0:
            person = Person.objects.filter(telegram_id=user_id).first()
        elif Person.objects.filter(name=name, telegram_id__isnull=True).count() > 0:
            person = Person.objects.filter(name=name).first()
        else:
            person = Person()

        person.name = name
        person.phone = phone
        person.telegram_id = user_id
        person.description = workname
        person.is_active = False
        person.save()

        azs = Azs.objects.filter(name=workname)
        if azs:
            employees = EmployeesAZK.objects.filter(person=person)
            if employees:
                empl = employees[0]
            else:
                empl = EmployeesAZK()
            empl.azk = azs[0]
            empl.person = person
            empl.save()

        answer = "Информация сохранена.\n"
        return person, answer
    else:
        answer = "Очень жаль."
        return None, answer


def dialog_start(user_id):
    person, answer = yield from get_person(user_id)
    if person:
        if not answer:
            answer += "\nЗдравствуйте %s!" % person
        answer += "\nЧтобы узнать что я умею введите /help"

    return answer


def dialog_register(user_id):
    person, answer = yield from hello(user_id)
    return answer


def dialog_accept(user_id):
    person, answer = yield from get_person(user_id)
    if isinstance(person, Person) and person.hr and person.is_active:
        answer = yield "Введите telegram_id, который вы хотите авторизовать:"
        try:
            person_id = int(answer.text)
            person = Person.objects.get(telegram_id=person_id)
            result, info = get_person_info(person)
            if result:
                saved = yield from ask_yes_or_no(info + "\n\n Авторизовываем? \n")
                if saved:
                    person.is_active = True
                    person.save()
                    answer = "Сотрудник аторизован.\n"
                else:
                    answer = "Отмена авторизации.\n"
        except:
            answer = "Код не найден."
    else:
        answer = "У Вас нет права авторизовывать."

    e = GeneratorExit(answer)
    raise e


def dialog_me(user_id):
    person, answer = yield from get_person(user_id)

    result, info = get_person_info(person)
    if result:
        answer += info

    return answer


def send_ticket(ticket_text):
    noticies = SlackNotice.objects.filter(type=SlackNotice.TBOT_ORDER)
    attachments = [
        {
            'fields': [
                {
                    "title": ticket_text,
                    "short": False,
                },
            ],
        },
    ]
    for notice in noticies:
        notice.send('Новая заявка:', attachments)


def dialog_ticket(user_id):
    person, answer = yield from get_person(user_id)

    if person and person.is_active:
        text = ''
        if not answer:
            text = '\nЗдравствуйте %s.' % person
        answer = yield '%s \nОпишите вашу проблему.' % text
        ticket_text = answer.text
        answer = yield from ask_yes_or_no("Отправляем заявку в службу техподдержки?")
        if answer:
            send_ticket(ticket_text)
            answer = 'Заявка отправлена.'
        else:
            answer = 'Заявка отменена.'
    else:
        answer += '\nЗаявка отменена. Заявки могут подавать только авторизованные пользователи.'

    e = GeneratorExit(answer)
    raise e


def ask_yes_or_no(question):
    """Спросить вопрос и дождаться ответа, содержащего «да» или «нет».
    Возвращает:
        bool
    """
    answer = yield (question, ["Да.", "Нет."])
    # while not ("да" in answer.text.lower() or "нет" in answer.text.lower()):
    #     answer = yield HTML("Так <b>да</b> или <b>нет</b>?")
    return "да" in answer.text.lower()


def discuss_good_python(name):
    answer = yield "Мы с вами, %s, поразительно похожи! Что вам нравится в нём больше всего?" % name
    likes_article = yield from ask_yes_or_no("Ага. А как вам, кстати, статья на Хабре? Понравилась?")
    if likes_article:
        answer = yield "Чудно!"
    else:
        answer = yield "Жалко."
    return answer


def discuss_bad_python(name):
    answer = yield "Ай-яй-яй. %s, фу таким быть! Что именно вам так не нравится?" % name
    likes_article = yield from ask_yes_or_no(
        "Ваша позиция имеет право на существование. Статья "
        "на Хабре вам, надо полагать, тоже не понравилась?")
    if likes_article:
        answer = yield "Ну и ладно."
    else:
        answer = yield (
            "Что «нет»? «Нет, не понравилась» или «нет, понравилась»?",
            ["Нет, не понравилась!", "Нет, понравилась!"]
        )
        answer = yield "Спокойно, это у меня юмор такой."
    return answer
