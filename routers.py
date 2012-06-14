# -*- coding: utf-8 -*-
'''
Created on 21.09.2011

@author: gorodechnyj
'''
import random

class MasterSlaveRouter(object):
    ''' A router that sets up a simple master/slave configuration '''

    def db_for_read(self, model, **hints):
        "Point all read operations to a random slave"
        return random.choice(['default', 'slave'])

    def db_for_write(self, model, **hints):
        "Point all write operations to the master"
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation between two objects"
        return True

    def allow_syncdb(self, db, model):
        "Explicitly put all models on all databases."
        if db == 'default':
            return True
        return False