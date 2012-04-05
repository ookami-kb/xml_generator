# -*- coding: utf-8 -*
from django import forms
from django.contrib.admin import widgets

class DateRange(forms.Form):
    start = forms.DateField(required=False, widget=widgets.AdminDateWidget())
    stop = forms.DateField(required=False, widget=widgets.AdminDateWidget())