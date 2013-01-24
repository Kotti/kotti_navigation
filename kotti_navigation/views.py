from pyramid.view import view_config

from paste.deploy.converters import asbool

from fanstatic import kotti_navigation as resource_group

from kotti.resources import get_root
from kotti.security import get_user

from kotti_navigation import navigation_settings
from kotti_navigation import nav_slot


def get_children(context, request):

    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(settings['show_hidden_while_logged_in'])
    ex_cts = settings['exclude_content_types']

    if show_hidden and user:
        children = [child for child in context.children_with_permission(request)
                   if child.__class__ not in ex_cts]
    else:
        children = [child for child in context.children_with_permission(request)
                    if child.in_navigation and child.__class__ not in ex_cts]
    return children


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

    include_root = asbool(settings['include_root'])
    display_type = settings['display_type']
    show_dropdown_menus = asbool(settings['show_dropdown_menus'])
    label = settings['label']

    current_level = 2

    items = get_children(root, request)

    # In the if below, show_label may be reset for the case of the
    # root, so we use a different boolean to pass to the template, specifying
    # explicitly if the first nav list item is a label, so should get a colon:
    show_label = False
    label_is_context = False
    label_contains_context = False
    before_context = ''
    after_context = ''

    if display_type == 'horizontal':
        if label and not label in ['none', 'None', 'NONE', 'no', 'No', 'NO']:
            if len(context.children) > 0:
                if context.parent:
                    label_lower = label.lower()
                    if label_lower == 'context':
                        items = [context] + context.children
                        label_is_context = True
                    elif ('context' in label
                          or 'Context' in label
                          or 'CONTEXT' in label):
                        before_context, after_context = \
                                split_label_on_context(label)

                        items = [context] + context.children
                        label_contains_context = True
                    else:
                        items = [{'title': label}] + context.children
                    show_label = True
                else:
                    items = context.children
            else:
                items = []
        else:
            items = context.children
    else:
        if label and not label in ['none', 'None', 'NONE', 'no', 'No', 'NO']:
            if 'context' in label or 'Context' in label or 'CONTEXT' in label:
                before_context, after_context = split_label_on_context(label)
            show_label = True
        else:
            show_label = False

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if nav_slot == 'beforebodyend' else False

    return {'root': root,
            'use_container_class': use_container_class,
            'include_root': include_root,
            'display_type': display_type,
            'items': items,
            'show_label': show_label,
            'label_is_context': label_is_context,
            'label_contains_context': label_contains_context,
            'before_context': before_context,
            'after_context': after_context,
            'show_dropdown_menus': show_dropdown_menus,
            'current_level': current_level,
        }
