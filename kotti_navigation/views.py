from pyramid.exceptions import PredicateMismatch
from pyramid.view import view_config

from fanstatic import kotti_navigation as resource_group
from fanstatic import kotti_navigation_dropdown as dropdown_resource_group

from kotti.resources import get_root
from kotti.views.util import render_view

from kotti_settings.util import get_setting
from kotti_settings.util import show_in_context

from kotti_navigation.util import parse_label
from kotti_navigation.util import get_children
from kotti_navigation.util import get_lineage
from kotti_navigation.util import get_nav_class
from kotti_navigation.util import is_node_open


class Navigation(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.location = 'top'
        self.slot = getattr(self.request, 'kotti_slot', None)
        if self.slot is not None:
            self.location = self.slot

    @view_config(name='navigation-widget',
                 renderer='string')
    def navigation_widget(self):
        show_here = get_setting(self.location + '_show_in_context')
        show = show_in_context(show_here, self.context)

        if not show:
            raise PredicateMismatch()

        display_type = get_setting(self.location + '_display_type')
        if not display_type:
            raise PredicateMismatch()

        view_name = 'navigation-widget-' + display_type

        return render_view(self.context, self.request, name=view_name)

    @view_config(name='nav-recurse',
                 renderer='kotti_navigation:templates/nav_recurse.pt')
    def nav_recurse(self):
        """Recursive view for the "tree" display type.
        """
        display_manner = get_setting(self.location + '_display_manner', default='pills')
        options = get_setting(self.location + '_options', default=[])
        tree_is_open_all = 'open_all' in options
        nav_class = get_nav_class(self.location)

        return {'tree_is_open_all': tree_is_open_all,
                'is_node_open': is_node_open,
                'nav_class': nav_class,
                'children': get_children(self.context,
                                         self.request,
                                         self.location),
                }

    @view_config(name='nav-recurse-dropdown',
                 renderer='kotti_navigation:templates/nav_recurse_dropdown.pt')
    def nav_recurse(self):
        """Recursive view for the "tree" display type.
        """
        display_manner = get_setting(self.location + '_display_manner', default='pills')
        options = get_setting(self.location + '_options', default=[])
        tree_is_open_all = 'open_all' in options
        nav_class = get_nav_class(self.location)

        return {'tree_is_open_all': tree_is_open_all,
                'is_node_open': is_node_open,
                'nav_class': nav_class,
                'children': get_children(self.context,
                                         self.request,
                                         self.location),
                }

    @view_config(name='navigation-widget-tree',
                 renderer='kotti_navigation:templates/nav_widget_tree.pt')
    def navigation_widget_tree(self):
        """Views for display type "tree", continued:
          - These are the main views for the tree display type, each using the
            general navigation_widget_tree() view function.
          - The nav recurse view above is called from nav_widget_tree.pt,
            used in each of these.
        """
        resource_group.need()
        root = get_root()

        display_type = get_setting(self.location + '_display_type')
        options = get_setting(self.location + '_options')
        if 'dropdowns' in options:
            dropdown_resource_group.need()

        include_root = 'include_root' in options
        show_menu = 'show_menu' in options
        label = get_setting(self.location + '_label')
        if label:
            label = parse_label(self.context.title, label)

        # When the nav display is set to the beforebodyend slot, the class
        # for the containing div needs to be 'container' so it fits to the
        # middle span12 area for content. When nav is in any of the other
        # slots, no class is needed, because the inherited CSS works to fit
        # nav to the slot.
        use_container_class = self.location == 'beforebodyend'

        items = get_children(root, self.request, self.location)
        tree_is_open_all = 'open_all' in options
        nav_class = get_nav_class(self.location)

        return {'location': self.location,
                'root': root,
                'display_type': display_type,
                'include_root': include_root,
                'show_menu': show_menu,
                'show_divider': show_menu and self.location != 'top' and items,
                'nav_class': nav_class,
                'tree_is_open_all': tree_is_open_all,
                'is_node_open': is_node_open,
                'use_container_class': use_container_class,
                'items': items,
                'label': label,
                'dropdowns': 'dropdowns' in options,
                'hidden': ''}

    @view_config(name='navigation-widget-items',
                 renderer='kotti_navigation:templates/nav_widget_items.pt')
    def navigation_widget_items(self):
        """Views for the "items" display type, a term used to avoid confusion
           that comes with calling this a "list" -- there are horizontal lists
           and there are vertical aspect lists. We distinguish here that the
           following views are not recursive and tree-like. They offer a
           limited list of items for the current context.
           - They each use the general navigation_widget_items() view function.
        """
        resource_group.need()

        display_type = get_setting(self.location + '_display_type')
        options = get_setting(self.location + '_options', default=[])
        nav_class = get_nav_class(self.location)

        # When the nav display is set to the beforebodyend slot, the class
        # for the containing div needs to be 'container' so it fits to the
        # middle span12 area for content. When nav is in any of the other
        # slots, no class is needed, because the inherited CSS works to fit
        # nav to the slot.
        use_container_class = self.location == 'beforebodyend'

        items = get_children(self.context, self.request, self.location)

        allowed_children = []
        for item in items:
            ac = get_children(item, self.request, self.location)
            allowed_children.append(ac if ac else [])

        label = parse_label(self.context.title,
                            get_setting(self.location + '_label'))

        careted = (display_type == 'items') and\
                    ('dropdowns' in options)

        return {'location': self.location,
                'items': items,
                'display_type': display_type,
                'nav_class': nav_class,
                'use_container_class': use_container_class,
                'show_menu': 'show_menu' in options,
                'allowed_children': allowed_children,
                'label': label,
                'dropdowns': 'dropdowns' in options,
            }

    @view_config(name='navigation-widget-breadcrumbs',
             renderer='kotti_navigation:templates/nav_widget_breadcrumbs.pt')
    def navigation_widget_breadcrumbs(self):
        """Views for the "breadcrumbs" display type, which is essentially the
           same as Kotti's default breadcrumbs display, except that here you
           have control of the associated label.
             - They each use the general navigation_widget_breadcrumbs()
               function.
        """
        resource_group.need()
        root = get_root()
        options = get_setting(self.location + '_options', default=[])
        include_root = 'include_root' in options
        label = parse_label(self.context.title,
                            get_setting(self.location + '_label'))

        # When the nav display is set to the beforebodyend slot, the class
        # for the containing div needs to be 'container' so it fits to the
        # middle span12 area for content. When nav is in any of the other
        # slots, no class is needed, because the inherited CSS works to fit
        # nav to the slot.
        use_container_class = self.location == 'beforebodyend'

        lineage_items = get_lineage(self.context, self.request, self.location)
        if not include_root and root in lineage_items:
            lineage_items.remove(root)

        lineage_items.reverse()

        return {'location': self.location,
                'use_container_class': use_container_class,
                'label': label,
                'lineage_items': lineage_items}

    @view_config(name='navigation-widget-menu',
                 renderer='kotti_navigation:templates/nav_widget_menu.pt')
    def navigation_widget_menu(self):
        """Views for the "menu" display type, which consists of a single button
           with a dropdown for presenting a full site context menu.
           - They each use the general navigation_widget_menu() view function.
           - The menu can be used standalone as the only nav display in a given
             location, or it can be combined with a label and/or another
             display type, e.g. a horizontal items nav display.
        """
        resource_group.need()
        root = get_root()
        options = get_setting(self.location + '_options', default=[])
        include_root = 'include_root' in options

        # When the nav display is set to the beforebodyend slot, the class
        # for the containing div needs to be 'container' so it fits to the
        # middle span12 area for content. When nav is in any of the other
        # slots, no class is needed, because the inherited CSS works to fit
        # nav to the slot.
        use_container_class = self.location == 'beforebodyend'

        items = get_children(self.context, self.request, self.location)

        top_level_items = get_children(root, self.request, self.location)

        # The lineage function of pyramid is used to make a breadcrumbs-style
        # display for the context menu.
        lineage_items = get_lineage(self.context, self.request, self.location)
        if not include_root and root in lineage_items:
            lineage_items.remove(root)

        # The lineage comes back in root-last order, so reverse.
        lineage_items.reverse()

        # The lineage (breadcrumbs style) display in navigation.pt shows
        # lineage_items in an indented dropdown list, and below that has a li
        # repeat on items, indented beneath context.

        return {'root': root,
                'location': self.location,
                'items': items,
                'use_container_class': use_container_class,
                'include_root': include_root,
                'top_level_items': top_level_items,
                'lineage_items': lineage_items}

    @view_config(name='navigation-widget-top',
                 renderer='kotti_navigation:templates/nav_widget_top.pt')
    def navigation_widget_top(self):
        """View for the special-case top location, which must be handled this
           way because Kotti's own default nav display must be overridden, and
           because the top location is not a simple "slot." It consists of a
           navbar at the very top, and a div location underneath that, as used
           here. The menu (represented by a single button) is appropriate for
           use within the navbar, but not so for the other display types, which
           are put in the div underneath.
           The driver for these views is the overridden nav.pt, which you will
           find in /kotti-overrides/templates/view/nav.pt.
        """
        display_type = get_setting(self.location + '_display_type')

        options = get_setting(self.location + '_options', default=[])
        include_root = 'include_root' in options
        label = get_setting(self.location + '_label')
        show_menu = 'show_menu' in options

        top_properties = {}

        if display_type == 'items':
            tree_properties = self.navigation_widget_items()

        elif display_type == 'tree' and 'list' in options:
            tree_properties = self.navigation_widget_items()

        elif display_type == 'tree':
            display_manner = get_setting(self.location + '_display_manner')
            tree_is_open_all = 'open_all' in options

            tree_properties = self.navigation_widget_tree()

            tree_properties['nav_class'] = \
                'nav nav-{0} nav-stacked'.format(display_manner)
            tree_properties['tree_is_open_all'] = tree_is_open_all
            tree_properties['is_node_open'] = is_node_open

            top_properties = tree_properties

        elif display_type == 'breadcrumbs':
            top_properties = self.navigation_widget_breadcrumbs()

        elif display_type == 'menu':
            top_properties = self.navigation_widget_menu()

        top_properties['location'] = 'top'
        top_properties['display_type'] = display_type
        top_properties['include_root'] = include_root
        top_properties['label'] = label
        top_properties['show_menu'] = show_menu

        return top_properties
