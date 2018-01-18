from django.http import Http404
from django.shortcuts import render, render_to_response
from django.template import loader

from orders.forms import OrderForm, OrderAllAzkForm
from main.models import Azs
from django.core import mail


def sendOrders(azkQuery, text_order, persone=""):
    msg_list = []
    # Если кол-во АЗК в списке больше 0
    if azkQuery.count() > 0:
        # Цикл по списку АЗК
        for azsObj in azkQuery:
            # Если инициатор в форме не заполнен, то берем Ответственного из карточки АЗК
            manager = persone
            if not manager:
                manager = azsObj.manager

            # Переменные для текста заявки
            context = {
                "name_contragent": "АО Иркутскнефтепродукт",
                "name_object": azsObj.full_name,
                "name_persone": manager,
                "phone": azsObj.phone,
                "location": "сервер",
                "order_type": "Запрос на обслуживание",
                "order_priority": "Стандартный",
                "problem": text_order
            }
            # Формируем тело письма из HTML шаблона
            html_content = loader.render_to_string('orders/sendOrderText.html', context)
            subject = "Заявка"
            mail_from = azsObj.eMail
            # mail_to = 'FalichevAYu@irknp.rosneft.ru'
            mail_to = 'krsdisp@rn-inform.ru'

            # создаем экземпляр письма и добавляем его в список на отправление
            msg = mail.EmailMessage(subject, html_content, mail_from, [mail_to])
            msg.content_subtype = 'html'
            msg_list.append(msg)

        try:
            # получаем коннект SMTP из настроек
            connection = mail.get_connection()
            connection.open()
            # отправляем список писем, res возвращает количество отправленных писем
            res = connection.send_messages(msg_list)
            connection.close()
            return res
        except:
            return -1


def orderOneAzk(request, azk):
    # в зависимости от значения count_send_msg выводится информация
    # -1 ошибка
    # 0 ничего
    # кол-во отправленных писем
    count_send_msg = 0

    # получаем №АЗК по началу e-mail например /order/azk91
    azkQuery = Azs.objects.filter(eMail__startswith=azk)
    # из всех найденных записей выбираем первую
    # если записей не нашли, то возвращаем пустую форму
    if azkQuery.count() > 0:
        azkObj = azkQuery.first()
        form = OrderForm(request.POST or None, initial={"fio": azkObj.manager})
        if request.POST:
            if form.is_valid():
                # Данные по заявке
                persone = form['fio'].value()
                text_order = form['text'].value()
                azkQuery = Azs.objects.filter(id=azkObj.id)
                # отправляем заявки
                count_send_msg = sendOrders(azkQuery, text_order, persone)
        return render(request, 'orders/order_one_azk.html',
                      {'form': form, "count_send_msg": count_send_msg, 'azk': azkObj, "path": request.get_host()})
    else:
        raise Http404


def orderAllAzk(request):
    # в зависимости от значения count_send_msg выводится информация
    # -1 ошибка
    # 0 ничего
    # кол-во отправленных писем
    count_send_msg = 0
    form = OrderAllAzkForm(request.POST or None)

    if request.GET:
        if 'mail' in request.GET:
            azk = request.GET['mail']
        else:
            azk = "None"
        return orderOneAzk(request, azk)

    if request.POST:
        if form.is_valid():
            # отправляем заявки
            # Получаем список АЗК и данные по заявке
            azkDict = form['azk'].value()
            persone = form['fio'].value()
            text_order = form['text'].value()
            azkQuery = Azs.objects.filter(id__in=azkDict)
            count_send_msg = sendOrders(azkQuery, text_order, persone)


    return render(request, 'orders/order_all_azk.html',
                  {'form': form, "count_send_msg": count_send_msg, "path": request.get_host()})
