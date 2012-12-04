from fanstatic import Library
from fanstatic import Resource

from paste.deploy.converters import asbool
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config

from kotti import _resolve_dotted
from kotti.resources import get_root
from kotti.security import get_user
from kotti.static import view_needed
from kotti.util import extract_from_settings
from kotti.views.slots import assign_slot

from logging import getLogger
log = getLogger('kotti_navigation: ')

_ = TranslationStringFactory('kotti_navigation')

NAVIGATION_WIDGET_DEFAULTS = {
    'include_root': 'true',
    'open_all': 'false',
    'show_hidden_while_logged_in': 'false',
    'exclude_content_types': '',
    }

library = Library("kotti_navigation", "static")
kotti_navigation_css = Resource(library, "style.css")
view_needed.add(kotti_navigation_css)


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_navigation.include_navigation_widget'


def navigation_settings(name=''):
    prefix = 'kotti_navigation.navigation_widget.'
    if name:
        prefix += name + '.'  # pragma: no cover
    settings = NAVIGATION_WIDGET_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    _resolve_dotted(settings, ['exclude_content_types'])
    return settings


def get_children(context, request):
    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(settings['show_hidden_while_logged_in'])
    ex_cts = settings['exclude_content_types']

    if show_hidden and user:
        childs = [child for child in context.children_with_permission(request)
                   if child.__class__ not in ex_cts]
    else:
        childs = [child for child in context.children_with_permission(request)
                    if child.in_navigation and child.__class__ not in ex_cts]
    return childs


def open_tree(item, request):
    """ Check if the tree should be opened for the given item.
    """
    # if all_open is true this is always True
    if asbool(navigation_settings()['open_all']):
        return True

    context = request.context

    root = get_root()
    open_tree = False
    while 1:
        if item == context:
            open_tree = True
            break
        if root == context:
            break
        if not hasattr(context, '__parent__'):
            break
        context = context.__parent__
    return open_tree


@view_config(name='nav-tree',
             renderer='kotti_navigation:templates/nav_tree.pt')
def nav_tree(context, request):
    return {'open_tree': open_tree,
            'children': get_children(context, request),
            }


@view_config(name='navigation-widget',
             renderer='kotti_navigation:templates/navigation.pt')
def navigation_widget(context, request, name=''):
    settings = navigation_settings()

    root = get_root()

    include_root = asbool(settings['include_root'])
    current_level = 2

    children = get_children(root, request)

    return {'root': root,
         'children': children,
         'include_root': include_root,
         'current_level': current_level,
        }


def include_view(config):
    config.scan(__name__)
    config.add_static_view('static-kotti_navigation',
                           'kotti_navigation:static')


def include_navigation_widget(config, where='left'):  # pragma: no cover
    include_view(config)
    assign_slot('navigation-widget', where)


def include_navigation_widget_right(config):  # pragma: no cover
    include_navigation_widget(config, 'right')
