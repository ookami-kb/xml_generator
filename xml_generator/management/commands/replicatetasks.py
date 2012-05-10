__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from copy import deepcopy
from django.db.models import Q
from optparse import make_option
#import pytz
from django.utils.timezone import utc

class Command(BaseCommand):
    args = ''
    help = u'replicates task with period >0 '
    option_list = BaseCommand.option_list + (
        make_option('--limit', '-l', dest='limit', action='store', type='int', default=10,
            help=u'пердельное количество дней для реплицирования'),
        make_option('--user', '-u', dest='username', action='store', type='string', default='all',
            help=u'чьи задания реплицировать'),
        )

        #except Exception as e:
        #    raise CommandError('error : "%s" ' % str(e))
    def handle(self, *args, **options):
        #try:
        limit = options.get('limit')
        username= options.get('username')

        tasks = Task.objects.filter(is_pattern=True)
        print tasks.count()
        if username != 'all':
            tasks = tasks.filter(user__username=username)

        _dt = datetime.now().replace(tzinfo=utc)
        print _dt.weekday().__str__()
        for task in tasks:
            print task.date_to_execute.weekday().__str__()
            if task.date_to_execute.weekday() == _dt.weekday():
                try:
                    existed_task = Task.objects.get(user=task.user, date_to_execute__day= datetime.now().replace(tzinfo=utc).day)
                    print 'existed ' + existed_task.pk.__str__()

                except:
                    new_task = Task(period = task.period, date_to_execute= datetime.now().replace(tzinfo=utc), user=task.user)
                    new_task.save()
                    for sp in task.salepoint.all():
                        new_task.salepoint.add(sp)
                    task.period = 0
                    task.save()
                    print 'created:  ' + new_task.pk.__str__()




