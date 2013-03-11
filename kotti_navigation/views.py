from pyramid.view import view_config
from pyramid.location import lineage

from paste.deploy.converters import asbool

from fanstatic import kotti_navigation as resource_group

from kotti.resources import get_root
from kotti.security import get_user

from kotti_navigation import navigation_settings


def get_children(context, request):

    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(settings['show_hidden_while_logged_in'])
    ex_cts = settings['exclude_content_types']

    if show_hidden and user:
        children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in ex_cts]
    else:
        children = [c for c in context.children_with_permission(request)
                    if c.in_navigation and c.__class__ not in ex_cts]

    return children


def get_lineage(context, request):

    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(settings['show_hidden_while_logged_in'])
    ex_cts = settings['exclude_content_types']

    if show_hidden and user:
        items = [item for item in list(lineage(context))
                 if item.__class__ not in ex_cts]
    else:
        items = [item for item in list(lineage(context))
                 if item.in_navigation and item.__class__ not in ex_cts]

    return items


def is_tree_open(item, request):
    """ Check if the tree should be opened for the given item.
    """

    # if all_open is true this is always True
    if asbool(navigation_settings()['open_all']):
        return True

    context = request.context

    root = get_root()
    is_tree_open = False

    while 1:
        if item == context:
            is_tree_open = True
            break
        if root == context:
            break
        if not hasattr(context, '__parent__'):
            break
        context = context.__parent__

    return is_tree_open


@view_config(name='nav-tree',
             renderer='kotti_navigation:templates/nav_tree.pt')
def nav_tree(context, request):

    return {'is_tree_open': is_tree_open,
            'children': get_children(context, request),
            }


def split_label_on_context(label):
    """Splits a label string containing the word 'context', if present.
    """

    context_spelling = ''

    if 'context' in label:
        context_spelling = 'context'
    elif 'Context' in label:
        context_spelling = 'Context'
    elif 'CONTEXT' in label:
        context_spelling = 'CONTEXT'

    if context_spelling:
        return label.split(context_spelling)
    else:
        return ('', '')


@view_config(name='navigation-widget',
             renderer='kotti_navigation:templates/navigation.pt')
def navigation_widget(context, request, name=''):

    resource_group.need()

    settings = navigation_settings()

    root = get_root()

    top_level_items = []

    include_root = asbool(settings['include_root'])
    display_type = settings['display_type']
    slot = settings['slot']
    show_context_menu = asbool(settings['show_context_menu'])
    show_dropdown_menus = asbool(settings['show_dropdown_menus'])
    label = settings['label']

    before_context = ''
    after_context = ''

    if display_type == 'tree':
        items = get_children(root, request)
    else:
        top_level_items = get_children(root, request)
        items = get_children(context, request)

    if label:
        label_lower = label.lower()

        if label_lower == 'context':
            label = context.title
        elif ('context' in label
              or 'Context' in label
              or 'CONTEXT' in label):
            before_context, after_context = split_label_on_context(label)
            label = before_context + context.title + after_context

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if slot == 'beforebodyend' else False

    allowed_children = []
    for item in items:
        ac = get_children(item, request)
        allowed_children.append(ac if ac else [])

    # The lineage function of pyramid is used to make a breadcrumbs-style
    # display for the context menu.
    lineage_items = get_lineage(context, request)
    if not include_root:
        lineage_items.remove(root)

    # The lineage comes back in root-last order, so reverse.
    lineage_items.reverse()

    # The lineage (breadcrumbs style) display in navigation.pt shows
    # lineage_items in an indented dropdown list, and below that has a li
    # repeat on items, indented beneath context.

    return {'root': root,
            'slot': slot,
            'use_container_class': use_container_class,
            'include_root': include_root,
            'display_type': display_type,
            'items': items,
            'show_context_menu': show_context_menu,
            'top_level_items': top_level_items,
            'lineage_items': lineage_items,
            'allowed_children': allowed_children,
            'label': label,
            'show_dropdown_menus': show_dropdown_menus,
        }
