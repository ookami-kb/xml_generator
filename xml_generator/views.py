from django.core.management import call_command

__author__ = 'eugene'
# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse
import os, shutil
from lxml import etree
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.template.response import TemplateResponse

from django.conf import settings
global_path = settings.GLOBAL_PATH
import csv
from xml_generator.models import *
from django.core.management import call_command

@csrf_exempt
def generate_xml(request):
    call_command('newimport')


