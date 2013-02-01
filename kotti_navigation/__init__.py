from pyramid.i18n import TranslationStringFactory

from kotti import _resolve_dotted
from kotti.views.slots import assign_slot
from kotti.util import extract_from_settings

from logging import getLogger
log = getLogger('kotti_navigation: ')

_ = TranslationStringFactory('kotti_navigation')


NAVIGATION_WIDGET_DEFAULTS = {
    'include_root': 'true',
    'display_type': 'tree',
    'label': '',
    'show_context_menu': 'false',
    'show_dropdown_menus': 'false',
    'slot': 'left',
    'open_all': 'false',
    'show_hidden_while_logged_in': 'false',
    'exclude_content_types': '',
    }


def navigation_settings(name='', settings=None):

    prefix = 'kotti_navigation.navigation_widget.'
    if name:
        prefix += name + '.'  # pragma: no cover

    working_settings = NAVIGATION_WIDGET_DEFAULTS.copy()

    working_settings.update(extract_from_settings(prefix, settings=settings))

    _resolve_dotted(working_settings, ['exclude_content_types'])

    return working_settings


def kotti_configure(settings):

    nav_settings = navigation_settings(settings=settings)

    slot = nav_settings['slot']
    if slot is None:
        slot = 'none'

    nav_widget_directive = \
            'kotti_navigation.include_navigation_widget_{0}'.format(slot)

    settings['pyramid.includes'] += ' {0}'.format(nav_widget_directive)


def include_view(config):

    config.add_translation_dirs('kotti_navigation:locale')
    config.scan(__name__)


def include_navigation_widget(config, where='left'):  # pragma: no cover

    include_view(config)
    if where != 'none':
        assign_slot('navigation-widget', where)


def include_navigation_widget_left(config):  # pragma: no cover

    include_navigation_widget(config, 'left')


def include_navigation_widget_right(config):  # pragma: no cover

    include_navigation_widget(config, 'right')


def include_navigation_widget_abovecontent(config):  # pragma: no cover

    include_navigation_widget(config, 'abovecontent')


def include_navigation_widget_belowcontent(config):  # pragma: no cover

    include_navigation_widget(config, 'belowcontent')


def include_navigation_widget_beforebodyend(config):  # pragma: no cover

    include_navigation_widget(config, 'beforebodyend')

def include_navigation_widget_none(config):  # pragma: no cover

    include_navigation_widget(config, 'none')
