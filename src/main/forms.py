from sqlite3 import Date

from django import forms

from main.models import *


class AzsForm(forms.ModelForm):
    class Meta:
        model = Azs
        exclude = [""]


class InventForm(forms.ModelForm):
    class Meta:
        model = Invent
        exclude = [""]
