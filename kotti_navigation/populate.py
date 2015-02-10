import colander
import deform

from kotti import get_settings
from kotti.views.slots import assign_slot

from kotti_settings.util import add_settings
from kotti_settings.util import get_setting
from kotti_navigation import _


display_types = ((u'', _(u'Not enabled')),
                 (u'vertical', _(u'Vertical')),
                 (u'horizontal', _(u'Horizontal')),
                 (u'menu', _(u'Menu')),
                 (u'breadcrumbs', _(u'Breadcrumbs')),
                )
#X hor_tabs                     horizontal (items)    context children
#X hor_pills                    horizontal (items)    context children
#X hor_tabs_with_dropdowns      horizontal (items)    context children +1
#X hor_pills_with_dropdowns     horizontal (items)    context children +1
#X breadcrumbs                  horizontal (items)    path to context
#C ver_tabs_stacked             vertical (tree-like)  context children
#C ver_pills_stacked            vertical (tree-like)  context children
#C ver_tabs_stacked_open_all    vertical (tree-like)  entire hierarchy
#C ver_pills_stacked_open_all   vertical (tree-like)  entire hierarchy
#X ver_list                     vertical (items)      context children
#X menu                         button with caret     path to context +1
#                              firing dropdown menu


class DisplayType(colander.SchemaNode):
    default = u''
    missing = u''
    widget = deform.widget.SelectWidget(values=display_types)


class Label(colander.SchemaNode):
    default = u''
    missing = u''


options = ((u'list', _(u'List')),
           (u'pills', _(u'Pills')),
           (u'tabs', _(u'Tabs')),
           (u'stacked', _(u'Stacked')),
           (u'open_all', _(u'Open all')),
           (u'dropdowns', _(u'With Dropdowns')),
           (u'show_menu', _(u'Show Menu')),
           (u'include_root', _(u'Include root')),
           (u'show_hidden_while_logged_in', _(u'Show hidden while logged in')),
           )


class Options(colander.SchemaNode):
    widget = deform.widget.SelectWidget(values=options,
                                        multiple=True)
    default = []
    missing = []


@colander.deferred
def deferred_content_types_widget(node, kw):
    types = get_settings()['kotti.available_types']
    values = [(type_, type_.type_info.name) for type_ in types]
    widget = deform.widget.SelectWidget(values=values,
                                        multiple=True)
    return widget


class ContentTypes(colander.SchemaNode):
    widget = deferred_content_types_widget
    default = []
    missing = []


class ShowHiddenWhileLoggedIn(colander.SchemaNode):
    default = False
    missing = False


class NavigationSchemaTop(colander.MappingSchema):
    top_display_type = DisplayType(colander.String(),
                             name=u'top_display_type',
                             title=_(u'Display type'))
    top_options = Options(colander.Set(),
                            name=u'top_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    top_exclude = ContentTypes(colander.Set(),
                            name=u'top_exclude',
                            title=_(u'Exclude Content Types'))
    top_include = ContentTypes(colander.Set(),
                            name=u'top_include',
                            title=_(u'Include Content Types'))
    top_label = Label(colander.String(),
                             name=u'top_label',
                             title=_(u'Label'))


class NavigationSchemaLeft(colander.MappingSchema):
    left_display_type = DisplayType(colander.String(),
                             name=u'left_display_type',
                             title=_(u'Display type'))
    left_options = Options(colander.Set(),
                            name=u'left_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    left_exclude = ContentTypes(colander.Set(),
                            name=u'left_exclude',
                            title=_(u'Exclude Content Types'))
    left_include = ContentTypes(colander.Set(),
                            name=u'left_include',
                            title=_(u'Include Content Types'))
    left_label = Label(colander.String(),
                             name=u'left_label',
                             title=_(u'Label'))


class NavigationSchemaRight(colander.MappingSchema):
    right_display_type = DisplayType(colander.String(),
                             name=u'right_display_type',
                             title=_(u'Display type'))
    right_options = Options(colander.Set(),
                            name=u'right_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    right_label = Label(colander.String(),
                             name=u'right_label',
                             title=_(u'Label'))
    right_exclude = ContentTypes(colander.Set(),
                            name=u'right_exclude',
                            title=_(u'Exclude Content Types'))
    right_include = ContentTypes(colander.Set(),
                            name=u'right_include',
                            title=_(u'Include Content Types'))


NavigationSettingsTop = {
    'name': 'navigation_settings_top',
    'title': _(u'Navigation Settings Top'),
    'description': _(u"Settings for navigation widget on the top"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaTop,
}

NavigationSettingsLeft = {
    'name': 'navigation_settings_left',
    'title': _(u'Navigation Settings Left'),
    'description': _(u"Settings for navigation widget in the left slot"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaLeft,
}

NavigationSettingsRight = {
    'name': 'navigation_settings_right',
    'title': _(u'Navigation Settings Right'),
    'description': _(u"Settings for navigation widget on the right"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaRight,
}


def populate():
    add_settings(NavigationSettingsTop)
    add_settings(NavigationSettingsLeft)
    add_settings(NavigationSettingsRight)
    if get_setting(u'left_display_type'):
        assign_slot('navigation-widget', 'left')
    if get_setting(u'right_display_type'):
        assign_slot('navigation-widget', 'right')
