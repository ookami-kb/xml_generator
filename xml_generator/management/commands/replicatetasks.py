__author__ = 'eugene'
# -*- coding: utf-8 -*-
from xml_generator.models import *
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from copy import deepcopy
from django.db.models import Q
from optparse import make_option


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
            print limit
            username= options.get('username')
            print username

            tasks = Task.objects.exclude(Q(period=0) | Q(period__isnull=True))
            if username != 'all':
                tasks = tasks.filter(user__username=username)
            for task in tasks:
                _date = task.date_to_execute
                repl_date = deepcopy(_date)
                while (repl_date - _date).days < limit:
                    repl_date += timedelta(days=task.period)
                    if repl_date.replace(tzinfo=None) > datetime.utcnow():
                        try:
                            existed_task = Task.objects.get(user=task.user, date_to_execute__day=repl_date.day)
                            existed_task.delete()
                            print 'deleted'
                        except:
                            pass

                        new_task = Task(period = 0, date_to_execute=repl_date, user=task.user)
                        new_task.save()
                        for sp in task.salepoint.all():
                            new_task.salepoint.add(sp)



        except Exception as e:
            raise CommandError('ho-ho, human, u will be assimilated: "%s" ' % str(e))