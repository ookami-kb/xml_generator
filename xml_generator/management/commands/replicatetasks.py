__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from copy import deepcopy
from django.db.models import Q
from optparse import make_option
import pytz

class Command(BaseCommand):
    args = ''
    help = u'replicates task with period >0 '
    option_list = BaseCommand.option_list + (
        make_option('--limit', '-l', dest='limit', action='store', type='int', default=10,
            help=u'пердельное количество дней для реплицирования'),
        make_option('--user', '-u', dest='username', action='store', type='string', default='all',
            help=u'чьи задания реплицировать'),
        )

    def handle(self, *args, **options):
        try:
            limit = options.get('limit')
            username= options.get('username')


            tasks = Task.objects.exclude(Q(period=0) | Q(period__isnull=True))
            if username != 'all':
                tasks = tasks.filter(user__username=username)
            for task in tasks:
                repl_date = deepcopy(task.date_to_execute)
                #print '1 '+ repl_date.day.__str__()
                #print '2: ' + datetime.utcnow().replace(tzinfo=pytz.utc).day.__str__()
                while repl_date < datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=limit):
                    #print task.pk.__str__() + ' - ' + repl_date.day.__str__()
                    if repl_date.day == datetime.utcnow().replace(tzinfo=pytz.utc).day:
                        try:
                            existed_task = Task.objects.get(user=task.user, date_to_execute__day=repl_date.day)
                            #print 'existed '
                        except:
                            new_task = Task(period = task.period, date_to_execute=repl_date, user=task.user)
                            new_task.save()
                            for sp in new_task.salepoint.all():
                                new_task.salepoint.add(sp)

                            print 'created:  ' + new_task.pk.__str__()

                    repl_date += timedelta(days=task.period)


        except Exception as e:
            raise CommandError('error : "%s" ' % str(e))