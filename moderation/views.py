from django.template.response import TemplateResponse
from xml_generator.models import Product
from django.contrib.auth.models import User

def dashboard(request):
    _context = {}
    return TemplateResponse(request, template='', context=_context)