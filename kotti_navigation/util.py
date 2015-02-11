from pyramid.events import subscriber
from pyramid.location import lineage

from kotti.resources import get_root
from kotti.security import get_user

from kotti_settings.events import SettingsAfterSave
from kotti_settings.util import get_setting


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


def the_user(request):
    return get_user(request)


def _check_children(request, location, children):
    user = the_user(request)
    options = get_setting(location + '_options', default=[])
    show_hidden = 'show_hidden_while_logged_in' in options
    content_types_to_include = get_setting(location + '_include')
    content_types_to_exclude = get_setting(location + '_exclude')

    if not (show_hidden and user):
        children = [c for c in children if c.in_navigation]
    if content_types_to_include:
        children = [c for c in children
                    if str(c.__class__) in content_types_to_include]
    if content_types_to_exclude:
        children = [c for c in children
                    if str(c.__class__) not in content_types_to_exclude]
    return children


def get_children(context, request, location):
    """Returns the children of a given context depending on the
       global settings and the optional location.
    """
    children = context.children_with_permission(request)
    return _check_children(request, location, children)


def get_lineage(context, request, location):
    items = list(lineage(context))
    return _check_children(request, location, items)


def is_node_open(item, request):
    """Check if the item (node in the "tree") should be opened. The page
       template code first checks if tree_is_open_all before this call,
       so we do not have to check that here. We assume it is False, and
       nodes must be checked individually.
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


def get_nav_class(options):
    """Build up a nav class for the navigation items based on the given
       options.
    """
    nav_class = 'nav'
    if 'list' in options:
        nav_class += ' nav-list'
    elif 'pills' in options:
        nav_class += ' nav-pills'
    elif 'tabs' in options:
        nav_class += ' nav-tabs'
    if 'stacked' in options:
        nav_class += ' nav-stacked'
    return nav_class


@subscriber(SettingsAfterSave)
def set_assigned_slot(event):
    """Reset the widget to the enabled slots."""
    #assign_slot('navigation-widget', slot)
