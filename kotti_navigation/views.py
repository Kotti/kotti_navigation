from pyramid.view import view_config

from paste.deploy.converters import asbool

from fanstatic import kotti_navigation as resource_group

from kotti.resources import get_root

from kotti_navigation import navigation_settings
from kotti_navigation.util import location_from_path
from kotti_navigation.util import parse_label
from kotti_navigation.util import get_children
from kotti_navigation.util import get_lineage
from kotti_navigation.util import is_node_open


@view_config(name='nav-recurse',
             renderer='kotti_navigation:templates/nav_recurse.pt')
def nav_recurse(context, request):
    """Recursive view for the "tree" display type.
    """
    if 'navigation-widget' in request.path:
        location = location_from_path(request.path)
    else:
        location = 'top'

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


@view_config(name='navigation-widget-tree-top',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
@view_config(name='navigation-widget-tree-left',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
@view_config(name='navigation-widget-tree-right',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
@view_config(name='navigation-widget-tree-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
@view_config(name='navigation-widget-tree-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
@view_config(name='navigation-widget-tree-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_tree.pt')
def navigation_widget_tree(context, request, name=''):
    """Views for display type "tree", continued:
      - These are the main views for the tree display type, each using the
        general navigation_widget_tree() view function.
      - The nav recurse view above is called from nav_widget_tree.pt,
        used in each of these.
    """
    # Assume top location, unless name or request.path are available.
    location = 'top'

    if name:
        location = name[name.rfind('-') + 1:]
    elif 'navigation-widget' in request.path:
        location = location_from_path(request.path)

    resource_group.need()

    root = get_root()

    settings = navigation_settings()

    # Set defaults:
    display_type = 'ver_tabs_stacked'
    include_root = False
    show_menu = False
    label = ''

    display_type_key = '{0}_display_type'.format(location)

    if display_type_key in settings:
        display_type = settings[display_type_key]

    include_root_key = '{0}_include_root'.format(location)
    if include_root_key in settings:
        include_root = asbool(settings[include_root_key])

    show_menu_key = '{0}_show_menu'.format(location)
    if show_menu_key in settings:
        show_menu = asbool(settings[show_menu_key])

    label_key = '{0}_label'.format(location)
    if label_key in settings:
        label = parse_label(context.title, settings[label_key])

    # When the nav display is set to the beforebodyend slot, the class for the
    # containing div needs to be 'container' so it fits to the middle span12
    # area for content. When nav is in any of the other slots, no class is
    # needed, because the inherited CSS works to fit nav to the slot.
    use_container_class = True if location == 'beforebodyend' else False

    items = get_children(root, request, location)

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
@view_config(name='navigation-widget-items-left',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
@view_config(name='navigation-widget-items-right',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
@view_config(name='navigation-widget-items-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
@view_config(name='navigation-widget-items-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
@view_config(name='navigation-widget-items-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_items.pt')
def navigation_widget_items(context, request, name=''):
    """Views for the "items" display type, a term used to avoid confusion
       that comes with calling this a "list" -- there are horizontal lists and
       there are vertical aspect lists. We distinguish here that the following
       views are not recursive and tree-like. They offer a limited list of
       items for the current context.
       - They each use the general navigation_widget_items() view function.
    """

    # Assume top location, unless name or request.path are available.
    location = 'top'

    if name:
        location = name[name.rfind('-') + 1:]
    elif 'navigation-widget' in request.path:
        location = location_from_path(request.path)

    resource_group.need()
    settings = navigation_settings()
    display_type = settings['{0}_display_type'.format(location)]
    show_menu = asbool(settings['{0}_show_menu'.format(location)])
    label = parse_label(context.title, settings['{0}_label'.format(location)])

    nav_class = 'nav nav-tabs'
    dropdowns = False

    if 'hor_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        nav_class = 'nav nav-{0}'.format(tabs_or_pills)
        dropdowns = True if display_type.endswith('downs') else False

    elif display_type == 'ver_list':

        nav_class = 'nav nav-list'
        dropdowns = True if display_type.endswith('downs') else False

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
@view_config(name='navigation-widget-breadcrumbs-left',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
@view_config(name='navigation-widget-breadcrumbs-right',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
@view_config(name='navigation-widget-breadcrumbs-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
@view_config(name='navigation-widget-breadcrumbs-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
@view_config(name='navigation-widget-breadcrumbs-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
def navigation_widget_breadcrumbs(context, request, name=''):
    """Views for the "breadcrumbs" display type, which is essentially the
       same as Kotti's default breadcrumbs display, except that here you have
       control of the associated label.
         - They each use the general navigation_widget_breadcrumbs() function.
    """
    # Assume top location, unless name or request.path are available.
    location = 'top'

    if name:
        location = name[name.rfind('-') + 1:]
    elif 'navigation-widget' in request.path:
        location = location_from_path(request.path)

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
    if not include_root and root in lineage_items:
        lineage_items.remove(root)

    lineage_items.reverse()

    return {'location': location,
            'use_container_class': use_container_class,
            'label': label,
            'lineage_items': lineage_items}


@view_config(name='navigation-widget-menu-top',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
@view_config(name='navigation-widget-menu-left',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
@view_config(name='navigation-widget-menu-right',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
@view_config(name='navigation-widget-menu-abovecontent',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
@view_config(name='navigation-widget-menu-belowcontent',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
@view_config(name='navigation-widget-menu-beforebodyend',
             renderer='kotti_navigation:templates/nav_widget_menu.pt')
def navigation_widget_menu(context, request, name=''):
    """Views for the "menu" display type, which consists of a single button
       with a dropdown for presenting a full site context menu.
       - They each use the general navigation_widget_menu() view function.
       - The menu can be used standalone as the only nav display in a given
         location, or it can be combined with a label and/or another display
         type, e.g. a horizontal items nav display.
    """
    # Assume top location, unless name or request.path are available.
    location = 'top'

    if name:
        location = name[name.rfind('-') + 1:]
    elif 'navigation-widget' in request.path:
        location = location_from_path(request.path)

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
    if not include_root and root in lineage_items:
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


@view_config(name='navigation-widget-top',
             renderer='kotti_navigation:templates/nav_widget_top.pt')
def navigation_widget_top(context, request, name=''):
    """View for the special-case top location, which must be handled this way
       because Kotti's own default nav display must be overridden, and because
       the top location is not a simple "slot." It consists of a navbar at the
       very top, and a div location underneath that, as used here. The menu
       (represented by a single button) is appropriate for use within the
       navbar, but not so for the other display types, which are put in the div
       underneath.
       The driver for these views is the overridden nav.pt, which you will find
       in /kotti-overrides/templates/view/nav.pt.
    """
    settings = navigation_settings()

    display_type = settings['top_display_type']

    include_root = False
    label = ''
    show_menu = False

    if 'top_include_root' in settings:
        include_root = asbool(settings['top_include_root'])

    if 'top_label' in settings:
        label = parse_label(context.title, settings['top_label'])

    if 'top_show_menu' in settings:
        show_menu = asbool(settings['top_show_menu'])

    top_properties = {}

    if 'hor_' in display_type:

        tree_properties = navigation_widget_items(
                context, request, name='navigation-widget-items-top')

    elif display_type == 'ver_list':

        tree_properties = navigation_widget_items(
                context, request, name='navigation-widget-items-top')

    elif 'ver_' in display_type:

        tabs_or_pills = 'tabs' if 'tabs' in display_type else 'pills'
        tree_is_open_all = True if display_type.endswith('open_all') else False

        tree_properties = navigation_widget_tree(
                context, request, name='navigation-widget-tree-top')

        tree_properties['nav_class'] = \
            'nav nav-{0} nav-stacked'.format(tabs_or_pills)
        tree_properties['tree_is_open_all'] = tree_is_open_all
        tree_properties['is_node_open'] = is_node_open

        top_properties = tree_properties

    elif display_type == 'breadcrumbs':

        top_properties = navigation_widget_breadcrumbs(
                context, request, name='navigation-widget-breadcrumbs-top')

    elif display_type == 'menu':

        top_properties = navigation_widget_menu(
                context, request, name='navigation-widget-menu-top')

    top_properties['location'] = 'top'
    top_properties['display_type'] = display_type
    top_properties['include_root'] = include_root
    top_properties['label'] = label
    top_properties['show_menu'] = show_menu

    return top_properties
