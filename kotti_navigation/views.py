from pyramid.view import view_config
from pyramid.location import lineage

from paste.deploy.converters import asbool

from fanstatic import kotti_navigation as resource_group

from kotti.resources import get_root
from kotti.security import get_user

from kotti_navigation import navigation_settings


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


def parse_label(title, label):

    if label:

        if label == 'none':
            label = ''
        else:
            label_lower = label.lower()

            if label_lower == 'context':
                label = title
            elif 'context' in label_lower:
                before_context, after_context = split_label_on_context(label)
                label = before_context + title + after_context
    else:
        label = ''

    return label


def get_children(context, request, location):

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
                    if c.__class__ not in content_types_to_exclude and c.__class__ in content_types_to_include]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in content_types_to_exclude]
    else:
        if content_types_to_include:
            children = [c for c in context.children_with_permission(request)
                    if c.__class in content_types_to_include \
                            and c.in_navigation and c.__class__ not in content_types_to_exclude]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.in_navigation and c.__class__ not in content_types_to_exclude]

    return children


def get_lineage(context, request, location):

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
                 and item.__class in content_types_to_include]
        else:
            items = [item for item in list(lineage(context))
                 if item.__class__ not in content_types_to_exclude]
    else:
        if content_types_to_include:
            items = [item for item in list(lineage(context))
                 if item.in_navigation
                 and item.__class__ not in content_types_to_exclude]
        else:
            items = [item for item in list(lineage(context))
                 if item.__class__ in content_types_to_include \
                     and item.in_navigation
                     and item.__class__ not in content_types_to_exclude]

    return items


def is_node_open(item, request):
    """ Check if the item (node in the "tree") should be opened.
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


@view_config(name='nav-recurse-top',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_top(context, request):

    return nav_stacked(context, request, 'top')


@view_config(name='nav-recurse-left',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_left(context, request):

    return nav_stacked(context, request, 'left')


@view_config(name='nav-recurse-right',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_right(context, request):

    return nav_stacked(context, request, 'right')


@view_config(name='nav-recurse-abovecontent',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_abovecontent(context, request):

    return nav_stacked(context, request, 'abovecontent')


@view_config(name='nav-recurse-belowcontent',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_belowcontent(context, request):

    return nav_stacked(context, request, 'belowcontent')


@view_config(name='nav-recurse-beforebodyend',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse_beforebodyend(context, request):

    return nav_stacked(context, request, 'beforebodyend')


def nav_stacked(context, request, location):

    settings = navigation_settings()

    display_type = settings['{0}_display_type'.format(location)]
    tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
    tree_is_open_all = True if display_type.endswith('open_all') else False

    return {'location': location,
            'tree_is_open_all': tree_is_open_all,
            'is_node_open': is_node_open,
            'nav_class': 'nav nav-{0} {0}-stacked'.format(tabs_or_pills),
            'children': get_children(context, request, location),
            }


@view_config(name='navigation-top',
             renderer='kotti_navigation:templates/nav_top.pt')
def navigation_top(context, request, name=''):

    settings = navigation_settings()

    location = settings['top_location']

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    return {'location': location,
            'use_container_class': use_container_class,
            'show_top_nav': asbool(settings['show_top_nav'])}


@view_config(name='navigation-widget-top',
             renderer='kotti_navigation:templates/nav_widget_top.pt')
def navigation_widget_top(context, request, name=''):

    settings = navigation_settings()

    if 'top_display_type' in settings:
        display_type = settings['top_display_type']
    else:
        return {}

    if 'top_include_root' in settings:
        include_root = asbool(settings['top_include_root'])
    else:
        include_root = False

    if 'top_label' in settings:
        label = parse_label(context.title, settings['top_label'])
    else:
        label = ''

    if 'top_show_menu' in settings:
        show_menu = asbool(settings['top_show_menu'])
    else:
        show_menu = False

    top_properties = {}

    if 'hor_' in display_type:

        tree_properties = navigation_widget_items(
                context, request, name='', location='top')

    elif display_type == 'ver_list':

        tree_properties = navigation_widget_items(
                context, request, name='', location='top')

    elif 'ver_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        tree_is_open_all = True if display_type.endswith('open_all') else False

        tree_properties = navigation_widget_tree(
                context, request, name='', location='top')

        tree_properties['location'] = 'top'
        tree_properties['nav_class'] = \
            'nav nav-{0} nav-stacked'.format(tabs_or_pills)
        tree_properties['tree_is_open_all'] = tree_is_open_all
        tree_properties['is_node_open'] = is_node_open

        top_properties = tree_properties

    elif display_type == 'breadcrumbs':

        top_properties = navigation_widget_breadcrumbs(
                    context, request, name, location='top')

    elif display_type == 'menu':

        top_properties = navigation_widget_menu(
                    context, request, name, location='top')


    top_properties['display_type'] = display_type
    top_properties['include_root'] = include_root
    top_properties['label'] = label
    top_properties['show_menu'] = show_menu

    return top_properties


@view_config(name='navigation-widget-tree-top',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_top(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='top')


@view_config(name='navigation-widget-tree-left',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_left(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='left')


@view_config(name='navigation-widget-tree-right',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_right(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='right')


@view_config(name='navigation-widget-tree-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_abovecontent(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='abovecontent')


@view_config(name='navigation-widget-tree-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_belowcontent(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='belowcontent')


@view_config(name='navigation-widget-tree-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree_beforebodyend(context, request, name=''):

    return navigation_widget_tree(
            context, request, name='', location='beforebodyend')


def navigation_widget_tree(context, request, name='', location=''):

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

    display_type_key = '{0}_display_type'.format(location)
    if display_type_key in settings:
        display_type = settings[display_type_key]
    else:
        display_type = 'ver_tabs_stacked'

    include_root_key = '{0}_include_root'.format(location)
    if include_root_key in settings:
        include_root = asbool(settings[include_root_key])
    else:
        include_root = False

    show_menu_key = '{0}_show_menu'.format(location)
    if show_menu_key in settings:
        show_menu = asbool(settings[show_menu_key])
    else:
        show_menu = False

    label_key = '{0}_label'.format(location)
    if label_key in settings:
        label = parse_label(context.title, settings[label_key])
    else:
        label = ''

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    items = get_children(context, request, location)

    tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
    nav_class = 'nav nav-{0} nav-stacked'.format(tabs_or_pills)
    tree_is_open_all = True if display_type.endswith('open_all') else False

    return {'location': location,
            'root': root,
            'display_type': display_type,
            'include_root': include_root,
            'show_menu': show_menu,
            'nav_class': nav_class,
            'tree_is_open_all': tree_is_open_all,
            'is_node_open': is_node_open,
            'use_container_class': use_container_class,
            'items': items,
            'label': label}


@view_config(name='navigation-widget-items-top',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_top(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='top')


@view_config(name='navigation-widget-items-left',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_left(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='left')


@view_config(name='navigation-widget-items-right',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_right(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='right')


@view_config(name='navigation-widget-items-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_abovecontent(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='abovecontent')


@view_config(name='navigation-widget-items-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_belowcontent(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='belowcontent')


@view_config(name='navigation-widget-items-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_beforebodyend(context, request, name=''):

    return navigation_widget_items(
            context, request, name, location='beforebodyend')


def navigation_widget_items(context, request, name='', location=''):

    resource_group.need()

    settings = navigation_settings()

    display_type = settings['{0}_display_type'.format(location)]

    show_menu = asbool(settings['{0}_show_menu'.format(location)])

    label = parse_label(context.title, settings['{0}_label'.format(location)])

    if 'hor_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        nav_class = 'nav nav-{0}'.format(tabs_or_pills)
        dropdowns = True if display_type.endswith('downs') else False

    elif display_type == 'ver_list':

        nav_class = 'nav nav-list'
        dropdowns = True if display_type.endswith('downs') else False

    else:

        nav_class = 'nav nav-tabs'
        dropdowns = False


    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    items = get_children(context, request, location)

    allowed_children = []
    for item in items:
        ac = get_children(item, request, location)
        allowed_children.append(ac if ac else [])

    return {'location': location,
            'items': items,
            'display_type': display_type,
            'nav_class': nav_class,
            'use_container_class': use_container_class,
            'show_menu': show_menu,
            'allowed_children': allowed_children,
            'label': label,
            'show_item_dropdowns': dropdowns,
        }


@view_config(name='navigation-widget-breadcrumbs-top',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_top(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='top')


@view_config(name='navigation-widget-breadcrumbs-left',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_left(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='left')


@view_config(name='navigation-widget-breadcrumbs-right',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_right(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='right')


@view_config(name='navigation-widget-breadcrumbs-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_abovecontent(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='abovecontent')


@view_config(name='navigation-widget-breadcrumbs-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_belowcontent(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='belowcontent')


@view_config(name='navigation-widget-breadcrumbs-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_beforebodyend(context, request, name=''):

    return navigation_widget_breadcrumbs(
            context, request, name, location='beforebodyend')


def navigation_widget_breadcrumbs(context, request, name='', location=''):

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

    include_root = asbool(settings['{0}_include_root'.format(location)])

    label = parse_label(context.title, settings['{0}_label'.format(location)])

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    lineage_items = get_lineage(context, request, location)
    if not include_root:
        lineage_items.remove(root)

    lineage_items.reverse()

    return {'location': location,
            'use_container_class': use_container_class,
            'label': label,
            'lineage_items': lineage_items}


@view_config(name='navigation-widget-menu-top',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_top(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='top')


@view_config(name='navigation-widget-menu-left',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_left(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='left')


@view_config(name='navigation-widget-menu-right',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_right(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='right')


@view_config(name='navigation-widget-menu-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_abovecontent(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='abovecontent')


@view_config(name='navigation-widget-menu-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_belowcontent(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='belowcontent')


@view_config(name='navigation-widget-menu-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_beforebodyend(context, request, name=''):

    return navigation_widget_menu(
            context, request, name, location='beforebodyend')


def navigation_widget_menu(context, request, name='', location=''):

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

    include_root = asbool(settings['{0}_include_root'.format(location)])

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    items = get_children(context, request, location)

    top_level_items = get_children(root, request, location)

    # The lineage function of pyramid is used to make a breadcrumbs-style
    # display for the context menu.
    lineage_items = get_lineage(context, request, location)
    if not include_root:
        lineage_items.remove(root)

    # The lineage comes back in root-last order, so reverse.
    lineage_items.reverse()

    # The lineage (breadcrumbs style) display in navigation.pt shows
    # lineage_items in an indented dropdown list, and below that has a li
    # repeat on items, indented beneath context.

    return {'root': root,
            'location': location,
            'items': items,
            'use_container_class': use_container_class,
            'include_root': include_root,
            'top_level_items': top_level_items,
            'lineage_items': lineage_items}
