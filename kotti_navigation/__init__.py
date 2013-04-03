from pyramid.i18n import TranslationStringFactory

from kotti import _resolve_dotted
from kotti.views.slots import assign_slot
from kotti.util import extract_from_settings

from logging import getLogger
log = getLogger('kotti_navigation: ')

_ = TranslationStringFactory('kotti_navigation')

locations = ['top', 'left', 'right',
             'abovecontent', 'belowcontent', 'beforebodyend']

property_endings_and_defaults = [('_display_type', 'none'),
                                 ('_show_menu', 'false'),
                                 ('_label', ''),
                                 ('_include_root', 'true'),
                                 ('_show_hidden_while_logged_in', 'false'),
                                 ('_include_content_types', ''),
                                 ('_exclude_content_types', '')]

NAVIGATION_WIDGET_DEFAULTS = {}

for loc in locations:
    for ending, default in property_endings_and_defaults:
        NAVIGATION_WIDGET_DEFAULTS['{0}{1}'.format(loc, ending)] = default


def navigation_settings(name='', settings=None):

    prefix = 'kotti_navigation.navigation_widget.'
    if name:
        prefix += name + '.'  # pragma: no cover

    working_settings = NAVIGATION_WIDGET_DEFAULTS.copy()

    working_settings.update(extract_from_settings(prefix, settings=settings))

    _resolve_dotted(working_settings, ['top_include_content_types'])
    _resolve_dotted(working_settings, ['left_include_content_types'])
    _resolve_dotted(working_settings, ['right_include_content_types'])
    _resolve_dotted(working_settings, ['abovecontent_include_content_types'])
    _resolve_dotted(working_settings, ['belowcontent_include_content_types'])
    _resolve_dotted(working_settings, ['beforebodyend_include_content_types'])

    _resolve_dotted(working_settings, ['top_exclude_content_types'])
    _resolve_dotted(working_settings, ['left_exclude_content_types'])
    _resolve_dotted(working_settings, ['right_exclude_content_types'])
    _resolve_dotted(working_settings, ['abovecontent_exclude_content_types'])
    _resolve_dotted(working_settings, ['belowcontent_exclude_content_types'])
    _resolve_dotted(working_settings, ['beforebodyend_exclude_content_types'])

    return working_settings


def kotti_configure(settings):

    nav_settings = navigation_settings(settings=settings)

    # Assign slots. The top location is not a slot. It is handled specially.
    for slot in [u'left', u'right',
                 u'abovecontent', u'belowcontent', u'beforebodyend']:

        display_type = nav_settings['{0}_display_type'.format(slot)]

        if display_type and display_type != 'none':

            if 'hor_' in display_type or display_type == 'ver_list':

                view_name = 'navigation-widget-items-{0}'.format(slot)

            elif 'ver_' in display_type:

                view_name = 'navigation-widget-tree-{0}'.format(slot)

            elif display_type == 'breadcrumbs':

                view_name = 'navigation-widget-breadcrumbs-{0}'.format(slot)

            elif display_type == 'menu':

                view_name = 'navigation-widget-menu-{0}'.format(slot)

            assign_slot(view_name, slot)

    settings['pyramid.includes'] += ' kotti_navigation.include_navigation'

    # We override nav.pt.
    settings['kotti.asset_overrides'] = 'kotti_navigation:kotti-overrides/'


def include_navigation(config):  # pragma: no cover

    config.add_translation_dirs('kotti_navigation:locale')
    config.scan(__name__)
