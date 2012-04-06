# -*- coding: utf-8 -*
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User

class DateRange(forms.Form):
    start = forms.DateField(required=False, widget=widgets.AdminDateWidget(), label=u'Начальная дата')
    stop = forms.DateField(required=False, widget=widgets.AdminDateWidget(), label=u'Конечная дата')
    
class UserSelect(forms.Form):
    users = User.objects.all()
    USERS = [(u.id, u.username) for u in users]
    USERS.insert(0, ('', u'-- все --'))
    
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label=u'Пользователь')