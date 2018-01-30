# -*- coding: utf-8 -*-
from main.models import Person, EmployeesAZK, Azs


def hello(start_message):
    answer = yield "Здравствуйте! Давайте познакомимся? \nЯ Агент техподдержки Сибинтек.\nА Вы? \nНапишите свое полное ФИО?"
    name = str(answer.text)
    chat_id = int(answer.from_user['id'])
    answer = yield "Приятно познакомиться, %s.\nЕсли вы работаете на АЗК/АЗС, то напишите полный номер АЗК?\nНапример: 055\n\nЕсли в другом месте, то название вашей компании." % name
    workname = answer.text.lower()
    answer = yield "Напишите ваш номер телефона.\nНапример: 89025566777"
    phone = answer.text

    saved = yield from ask_yes_or_no("Сохраняем информацию о Вас?")
    if saved:

        if Person.objects.filter(telegram_id=chat_id).count()>0:
            person = Person.objects.filter(telegram_id=chat_id)[0]
        elif Person.objects.filter(name=name).count()>0:
            person = Person.objects.filter(name=name)[0]
        else:
            person = Person()

        person.name = name
        person.phone = phone
        person.telegram_id = chat_id
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
    else:
        answer = "Как скажите."

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
