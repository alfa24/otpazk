# -*- coding: utf-8 -*-
from main.models import Person, EmployeesAZK, Azs


def get_person(user_id):
    try:
        return Person.objects.get(telegram_id=user_id), ''
    except:
        person, answer = yield from hello(user_id)
        return person, answer


def hello(user_id):
    answer = yield "Здравствуйте! Мы еще не знакомы! \nЯ Агент техподдержки Сибинтек.\nА Вы? \nНапишите свое полное ФИО."
    name = str(answer.text)
    answer = yield "Приятно познакомиться, %s.\nЕсли вы работаете на АЗК/АЗС, то напишите полный номер АЗК?\nНапример: 055\n\nЕсли в другом месте, то название вашей компании." % name
    workname = answer.text.lower()
    answer = yield "Напишите ваш номер телефона.\nНапример: 89025566777"
    phone = answer.text

    saved = yield from ask_yes_or_no("Сохраняем информацию о Вас?")
    if saved:

        if Person.objects.filter(telegram_id=user_id).count() > 0:
            person = Person.objects.filter(telegram_id=user_id).first()
        elif Person.objects.filter(name=name).count() > 0:
            person = Person.objects.filter(name=name).first()
        else:
            person = Person()

        person.name = name
        person.phone = phone
        person.telegram_id = user_id
        person.description = workname
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

        answer = "Информация сохранена."
        return person, answer
    else:
        answer = "Очень жаль."
        return False, answer


def dialog_start(user_id):
    person, answer = yield from get_person(user_id)
    if person:
        if not answer:
            answer += "\nЗдравствуйте %s!" % person
        answer += "\nЧтобы узнать что я умею введите /help"

    return answer


def dialog_ticket(user_id):
    person, answer = yield from get_person(user_id)

    if person:
        text =''
        if not answer:
            text = '\nЗдравствуйте %s.' % person
        ticket_text = yield '%s \nОпишите вашу проблему.' % text

        answer = yield from ask_yes_or_no("Отправляем заявку в службу техподдержки?")
        if answer:
            # send ticket
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
