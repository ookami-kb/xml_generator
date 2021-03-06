# -*- coding: utf-8 -*
"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'xml_generator.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for xml_generator admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_(u'Главная'), reverse('admin:index')),
            items.AppList(
                _(u'Данные о продуктах и пр.'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _(u'Пользователи'),
                models=('django.contrib.*',)
            ),
            items.MenuItem(_(u'Статистика'), reverse('xml_generator.analytics.admin_views.users_stat')),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
