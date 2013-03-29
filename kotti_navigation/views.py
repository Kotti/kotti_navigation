from pyramid.view import view_config
from pyramid.location import lineage

from paste.deploy.converters import asbool

from fanstatic import kotti_navigation as resource_group

from kotti.resources import get_root
from kotti.security import get_user

from kotti_navigation import navigation_settings


def get_children(context, request):

    if len(request.POST.items()) == 0:
        location = 'top'
    else:
        location = 'left'
        for k,v in request.POST.items():
            if k == 'location':
                location = v

    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(
            settings['{0}_show_hidden_while_logged_in'.format(location)])
    in_cts = settings['{0}_include_content_types'.format(location)]
    ex_cts = settings['{0}_exclude_content_types'.format(location)]

    if show_hidden and user:
        if in_cts:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in ex_cts and c.__class__ in in_cts]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.__class__ not in ex_cts]
    else:
        if in_cts:
            children = [c for c in context.children_with_permission(request)
                    if c.__class in in_cts \
                            and c.in_navigation and c.__class__ not in ex_cts]
        else:
            children = [c for c in context.children_with_permission(request)
                    if c.in_navigation and c.__class__ not in ex_cts]

    return children


def get_lineage(context, request):

    if len(request.POST.items()) == 0:
        location = 'top'
    else:
        location = 'left'
        for k,v in request.POST.items():
            if k == 'location':
                location = v

    settings = navigation_settings()
    user = get_user(request)
    show_hidden = asbool(
            settings['{0}_show_hidden_while_logged_in'.format(location)])
    in_cts = settings['{0}_include_content_types'.format(location)]
    ex_cts = settings['{0}_exclude_content_types'.format(location)]

    if show_hidden and user:
        if in_cts:
            items = [item for item in list(lineage(context))
                 if item.__class__ not in ex_cts and item.__class in in_cts]
        else:
            items = [item for item in list(lineage(context))
                 if item.__class__ not in ex_cts]
    else:
        if in_cts:
            items = [item for item in list(lineage(context))
                 if item.in_navigation and item.__class__ not in ex_cts]
        else:
            items = [item for item in list(lineage(context))
                 if item.__class__ in in_cts \
                     and item.in_navigation and item.__class__ not in ex_cts]

    return items


def is_open(item, request):
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


def nav_stacked(context, request, tabs_or_pills, open):

    return {'is_open_all': open,
            'is_open': is_open,
            'nav_class': 'nav nav-{0} {0}-stacked'.format(tabs_or_pills),
            'nav_view': 'nav-{0}-stacked'.format(tabs_or_pills),
            'children': get_children(context, request),
            }


@view_config(name='nav-recurse-tabs-stacked',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_tabs_stacked(context, request):

    return nav_stacked(context, request, 'tabs', False)


@view_config(name='nav-recurse-tabs-stacked-open-all',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_tabs_stacked_open_all(context, request):

    return nav_stacked(context, request, 'tabs', True)


@view_config(name='nav-recurse-pills-stacked',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_pills_stacked(context, request):

    return nav_stacked(context, request, 'pills', False)


@view_config(name='nav-recurse-pills-stacked-open-all',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_pills_stacked_open_all(context, request):

    return nav_stacked(context, request, 'pills', True)


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


@view_config(name='navigation-widget',
             renderer='kotti_navigation:templates/nav_widget.pt')
def navigation_widget(context, request, name=''):

    return {'display_type': navigation_settings()['display_type']}


def navigation_widget_tree(context, request, name='', location=''):

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

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
        label = settings[label_key]
    else:
        label = ''

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

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

    return {'root': root,
            'include_root': include_root,
            'show_menu': show_menu,
            'aspect': 'vertical',
            'use_container_class': use_container_class,
            'items': items,
            'label': label}


@view_config(name='navigation-widget-tree',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_stacked(context, request, name=''):

    if len(request.POST.items()) == 0:

        location = 'top'
        display_type = navigation_settings()['top_display_type']
        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        is_open = True if display_type.endswith('open_all') else False

    else:

        for k,v in request.POST.items():
            if k == 'location':
                location = v
            elif k == 'tabs_or_pills':
                tabs_or_pills = v
            elif k == 'is_open':
                is_open = True if v == 'true' else False

    tree_properties = navigation_widget_tree(
            context, request, name='', location=location)

    tree_properties['location'] = location
    tree_properties['nav_class'] = \
            'nav nav-{0} nav-stacked'.format(tabs_or_pills)
    tree_properties['is_open'] = is_open
    tree_properties['nav_view'] = \
            'nav-recurse-{0}-stacked'.format(tabs_or_pills)

    return tree_properties


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
        label = settings['top_label']
    else:
        label = ''
    if 'top_show_menu' in settings:
        show_menu = asbool(settings['top_show_menu'])
    else:
        show_menu = False

    top_properties = {}

    if 'hor_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        dropdowns = True if display_type.endswith('downs') else False

        top_properties = navigation_widget_items(context, request, name,
            location='top', nav_class='nav nav-{0}'.format(tabs_or_pills),
            aspect='horizontal', dropdowns=dropdowns)

    elif display_type == 'ver_list':

        top_properties = navigation_widget_items(context, request, name,
            location='top', nav_class='nav nav-list',
            aspect='vertical', dropdowns=dropdowns)

    elif 'ver_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        is_open = True if display_type.endswith('open_all') else False

        tree_properties = navigation_widget_tree(
                context, request, name='', location='top')

        tree_properties['location'] = 'top'
        tree_properties['nav_class'] = \
            'nav nav-{0} nav-stacked'.format(tabs_or_pills)
        tree_properties['is_open'] = is_open
        tree_properties['nav_view'] = \
            'nav-recurse-{0}-stacked'.format(tabs_or_pills)

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


@view_config(name='navigation-widget-items',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items_for_slot(context, request, name=''):

    if len(request.POST.items()) == 0:

        location = 'top'
        display_type = navigation_settings()['top_display_type']
        aspect = \
            'vertical' if display_type.startswith('ver_') else 'horizontal'
        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        nav_class = 'nav nav-{0}'.format(tabs_or_pills)
        dropdowns = True if display_type.endswith('downs') else False

    else:

        for k,v in request.POST.items():
            if k == 'nav_class':
                nav_class = v
            elif k == 'location':
                location = v
            elif k == 'aspect':
                aspect = v
            elif k == 'dropdowns':
                dropdowns = True if v == 'true' else False

    return navigation_widget_items(context, request, name,
            location, nav_class, aspect, dropdowns)


def navigation_widget_items(context, request, name='',
        location='', nav_class='', aspect='', dropdowns=False):

    resource_group.need()

    settings = navigation_settings()

    show_menu = asbool(settings['{0}_show_menu'.format(location)])

    label = settings['{0}_label'.format(location)]

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

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

    allowed_children = []
    for item in items:
        ac = get_children(item, request)
        allowed_children.append(ac if ac else [])

    return {'location': location,
            'items': items,
            'aspect': aspect,
            'nav_class': nav_class,
            'use_container_class': use_container_class,
            'show_menu': show_menu,
            'allowed_children': allowed_children,
            'label': label,
            'show_item_dropdowns': dropdowns,
        }


@view_config(name='navigation-widget-breadcrumbs',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs_slot(context, request, name=''):

    if len(request.POST.items()) == 0:
        location = 'top'
    else:
        location = 'left'
        for k,v in request.POST.items():
            if k == 'location':
                location = v

    return navigation_widget_breadcrumbs(context, request, name, location)


def navigation_widget_breadcrumbs(context, request, name='', location=''):

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

    include_root = asbool(settings['{0}_include_root'.format(location)])
    label = settings['{0}_label'.format(location)]

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    lineage_items = get_lineage(context, request)
    if not include_root:
        lineage_items.remove(root)

    lineage_items.reverse()

    return {'location': location,
            'use_container_class': use_container_class,
            'label': label,
            'lineage_items': lineage_items}


@view_config(name='navigation-widget-menu',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu_slot(context, request, name=''):

    if len(request.POST.items()) == 0:
        location = 'top'
    else:
        location = 'left'
        for k,v in request.POST.items():
            if k == 'location':
                location = v

    return navigation_widget_menu(context, request, name, location)


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

    items = get_children(context, request)

    top_level_items = get_children(root, request)

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
            'location': location,
            'items': items,
            'use_container_class': use_container_class,
            'include_root': include_root,
            'top_level_items': top_level_items,
            'lineage_items': lineage_items}
