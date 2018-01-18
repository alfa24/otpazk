from sqlite3 import Date

from django import forms
from django.forms.utils import ErrorList

from main.models import Azs


class OrderForm(forms.Form):
    fio = forms.CharField(label='Инициатор', max_length=200, required=False)
    text = forms.CharField(label='Текст заявки', widget=forms.Textarea)


class OrderAllAzkForm(OrderForm):
    azk = forms.ModelMultipleChoiceField(queryset=Azs.objects.order_by('azs_group__name'), label="от АЗК")


