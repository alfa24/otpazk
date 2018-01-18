import datetime
from django.shortcuts import render

# Create your views here.
from main.forms import *
from main.models import *


def naliv(request):
    form = InventForm(request.GET or None)
    defaultStartDate = datetime.datetime.now().strftime("%dd.%mm.%Y 08:00")
    defaultEndDate = datetime.datetime.now().strftime("%dd.%mm.%Y 17:00")
    msg = ''

    if request.GET:
        if 'azs' in request.GET and 'dateStart' in request.GET and 'dateEnd' in request.GET:
            msg = saveEntry(request)
        elif 'id_invent' in request.GET and 'enbled' in request.GET:
            msg = updateEntry(request)
        elif 'ip' in request.GET:
            access = getAccess(request)
            return render(request, 'main/accessForInv.html', locals())

    invs = Invent.objects.all().order_by('-id')[0:100]
    return render(request, 'main/index.html', locals())


def formatIpAddress(ip):
    sp = ip.split('.')
    if len(sp) == 4:
        i0 = int(sp[0])
        i1 = int(sp[1])
        i2 = int(sp[2])
        i3 = int(sp[3])
        result = str(i0) + '.' + str(i1) + '.' + str(i2) + '.' + str(i3)
    else:
        result = '0.0.0.0'
    return result


def getAccess(request):
    ip = formatIpAddress(request.GET['ip'])
    try:
        azs_obj = Azs.objects.get(ipAddress=ip)
        current_date = datetime.datetime.now()
        q = Invent.objects.filter(azs=azs_obj)
        q = q.filter(enabled=True)
        q = q.filter(dateStart__lte=current_date)
        q = q.filter(dateEnd__gte=current_date)
        if q.count() > 0:
            return True
    except:
        return False

    return False


def updateEntry(request):
    try:
        i = Invent.objects.get(id=request.GET['id_invent'])
        i.enabled = request.GET['enbled']
        i.save()
        return "Инвентаризация отклечена"
    except:
        return "Запись не найдена"


def saveEntry(request):
    try:
        azs_obj = Azs.objects.get(id=request.GET['azs'])
        new_form = Invent()
        new_form.azs = azs_obj
        new_form.dateStart = datetime.datetime.strptime(request.GET['dateStart'], "%d.%m.%Y %H:%M")
        new_form.dateEnd = datetime.datetime.strptime(request.GET['dateEnd'], "%d.%m.%Y %H:%M")
        new_form.enabled = True
        new_form.save()
        return "Инвентаризация добавлена"
    except:
        return "Неверные параметры"
