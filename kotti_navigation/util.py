from paste.deploy.converters import asbool

from pyramid.location import lineage

from kotti.resources import get_root
from kotti.security import get_user

from kotti_navigation import navigation_settings


def location_from_path(path):

    view_name = path[path.rfind('/'):]

    location = None
    if 'top' in view_name:
        location = 'top'
    elif 'left' in view_name:
        location = 'left'
    elif 'right' in view_name:
        location = 'right'
    elif 'abovecontent' in view_name:
        location = 'abovecontent'
    elif 'belowcontent' in view_name:
        location = 'belowcontent'
    elif 'beforebodyend' in view_name:
        location = 'beforebodyend'

    return location


def parse_label(title, label):

    if not label or label == 'none':
        return ''
    else:
        label_lower = label.lower()

        if label_lower == 'context':
            return title
        elif 'context' in label_lower:
            # Replace context placeholder string with title:
            start = label_lower.index('context')
            return label[0:start] + title + label[start + 7:]
        else:
            return label


def get_children(context, request, location):

    # [TODO] Move these function calls out to caller.

    user = get_user(request)

    settings = navigation_settings()

    show_hidden = asbool(
            settings['{0}_show_hidden_while_logged_in'.format(location)])
    content_types_to_include = \
            settings['{0}_include_content_types'.format(location)]
    content_types_to_exclude = \
            settings['{0}_exclude_content_types'.format(location)]

    if show_hidden and user:
        if content_types_to_include:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in content_types_to_exclude
                    and c.__class__ in content_types_to_include]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in content_types_to_exclude]
    else:
        if content_types_to_include:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ in content_types_to_include
                            and c.in_navigation
                            and c.__class__ not in content_types_to_exclude]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.in_navigation
                    and c.__class__ not in content_types_to_exclude]

    return children


def get_lineage(context, request, location):

    # [TODO] Move these function calls out to caller.

    user = get_user(request)

    settings = navigation_settings()

    show_hidden = asbool(
            settings['{0}_show_hidden_while_logged_in'.format(location)])
    content_types_to_include = \
            settings['{0}_include_content_types'.format(location)]
    content_types_to_exclude = \
            settings['{0}_exclude_content_types'.format(location)]

    if show_hidden and user:
        if content_types_to_include:
            items = [item for item in list(lineage(context))
                 if item.__class__ not in content_types_to_exclude
                 and item.__class__ in content_types_to_include]
        else:
            items = [item for item in list(lineage(context))
                 if item.__class__ not in content_types_to_exclude]
    else:
        if content_types_to_include:
            items = [item for item in list(lineage(context))
                 if item.__class__ in content_types_to_include
                 and item.in_navigation
                 and item.__class__ not in content_types_to_exclude]
        else:
            items = [item for item in list(lineage(context))
                 if item.in_navigation
                 and item.__class__ not in content_types_to_exclude]

    return items


def is_node_open(item, request):
    """ Check if the item (node in the "tree") should be opened. The page
    template code first checks if tree_is_open_all before this call, so we do
    not have to check that here. We assume it is False, and nodes must be
    checked individually.
    """

    context = request.context

    root = get_root()
    is_open = False

    while 1:
        if item == context:
            is_open = True
            break
        if root == context:
            break
        if not hasattr(context, '__parent__'):
            break
        context = context.__parent__

    return is_open
