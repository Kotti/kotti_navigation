import colander
import deform

from kotti import get_settings
from kotti.views.slots import assign_slot

from kotti_settings.config import ShowInContextSchemaNode
from kotti_settings.util import add_settings
from kotti_settings.util import get_setting
from kotti_navigation import _


display_types = ((u'', _(u'Not enabled')),
                 (u'tree', _(u'Tree')),
                 (u'items', _(u'Items')),
                 (u'menu', _(u'Menu')),
                 (u'breadcrumbs', _(u'Breadcrumbs')),
                )


class DisplayType(colander.SchemaNode):
    widget = deform.widget.SelectWidget(values=display_types)
    default = u''
    missing = u''


class Label(colander.SchemaNode):
    default = u''
    missing = u''


display_manner = ((u'pills', _(u'Pills')),
                  (u'tabs', _(u'Tabs')))


class DisplayManner(colander.SchemaNode):
    widget = deform.widget.SelectWidget(values=display_manner)
    default = u'pills'
    missing = u'pills'


options = ((u'stacked', _(u'Stacked')),
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
    top_display_manner = DisplayManner(colander.String(),
                            name=u'top_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
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
    show_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'top_show_in_context')


class NavigationSchemaLeft(colander.MappingSchema):
    left_display_type = DisplayType(colander.String(),
                             name=u'left_display_type',
                             title=_(u'Display type'))
    left_display_manner = DisplayManner(colander.String(),
                            name=u'left_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
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
    show_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'left_show_in_context')


class NavigationSchemaRight(colander.MappingSchema):
    right_display_type = DisplayType(colander.String(),
                             name=u'right_display_type',
                             title=_(u'Display type'))
    right_display_manner = DisplayManner(colander.String(),
                            name=u'right_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
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
    show_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'right_show_in_context')


class NavigationSchemaAboveContent(colander.MappingSchema):
    abovecontent_display_type = DisplayType(colander.String(),
                             name=u'abovecontent_display_type',
                             title=_(u'Display type'))
    abovecontent_display_manner = DisplayManner(colander.String(),
                            name=u'abovecontent_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
    abovecontent_options = Options(colander.Set(),
                            name=u'abovecontent_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    abovecontent_label = Label(colander.String(),
                             name=u'abovecontent_label',
                             title=_(u'Label'))
    abovecontent_exclude = ContentTypes(colander.Set(),
                            name=u'abovecontent_exclude',
                            title=_(u'Exclude Content Types'))
    abovecontent_include = ContentTypes(colander.Set(),
                            name=u'abovecontent_include',
                            title=_(u'Include Content Types'))
    abovecontent_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'abovecontent_show_in_context')


class NavigationSchemaBelowContent(colander.MappingSchema):
    belowcontent_display_type = DisplayType(colander.String(),
                             name=u'bc_display_type',
                             title=_(u'Display type'))
    belowcontent_display_manner = DisplayManner(colander.String(),
                            name=u'belowcontent_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
    belowcontent_options = Options(colander.Set(),
                            name=u'bc_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    belowcontent_label = Label(colander.String(),
                             name=u'belowcontent_label',
                             title=_(u'Label'))
    belowcontent_exclude = ContentTypes(colander.Set(),
                            name=u'belowcontent_exclude',
                            title=_(u'Exclude Content Types'))
    belowcontent_include = ContentTypes(colander.Set(),
                            name=u'belowcontent_include',
                            title=_(u'Include Content Types'))
    belowcontent_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'belowcontent_show_in_context')


class NavigationSchemaBeforeBodyEnd(colander.MappingSchema):
    beforebodyend_display_type = DisplayType(colander.String(),
                             name=u'beforebodyend_display_type',
                             title=_(u'Display type'))
    beforebodyend_display_manner = DisplayManner(colander.String(),
                            name=u'beforebodyend_display_manner',
                            title=_(u'Display manner'),
                            description=_(u'Choose how the navigation will be displayed.'))
    beforebodyend_options = Options(colander.Set(),
                            name=u'beforebodyend_options',
                            title=_(u'Options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    beforebodyend_label = Label(colander.String(),
                             name=u'beforebodyend_label',
                             title=_(u'Label'))
    beforebodyend_exclude = ContentTypes(colander.Set(),
                            name=u'beforebodyend_exclude',
                            title=_(u'Exclude Content Types'))
    beforebodyend_include = ContentTypes(colander.Set(),
                            name=u'beforebodyend_include',
                            title=_(u'Include Content Types'))
    beforebodyend_in_context = ShowInContextSchemaNode(colander.String(),
                             name=u'beforebodyend_show_in_context')


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


NavigationSettingsAboveContent = {
    'name': 'navigation_settings_above_content',
    'title': _(u'Navigation Settings Above Content'),
    'description': _(u"Settings for navigation widget above the content"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaAboveContent,
}


NavigationSettingsBelowContent = {
    'name': 'navigation_settings_below_content',
    'title': _(u'Navigation Settings Below Content'),
    'description': _(u"Settings for navigation widget below the content"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaBelowContent,
}


NavigationSettingsBeforeBodyEnd = {
    'name': 'navigation_settings_before_body_end',
    'title': _(u'Navigation Settings Before Body End'),
    'description': _(u"Settings for navigation widget before body end"),
    'success_message': _(u"Successfully saved navigation widget settings."),
    'schema_factory': NavigationSchemaBeforeBodyEnd,
}


def populate():
    add_settings(NavigationSettingsLeft)
    add_settings(NavigationSettingsRight)
    add_settings(NavigationSettingsTop)
    add_settings(NavigationSettingsAboveContent)
    add_settings(NavigationSettingsBelowContent)
    add_settings(NavigationSettingsBeforeBodyEnd)

    if get_setting(u'left_display_type'):
        assign_slot(u'navigation-widget', 'left')
    if get_setting(u'right_display_type'):
        assign_slot(u'navigation-widget', 'right')
    if get_setting(u'abovecontent_display_type'):
        assign_slot(u'navigation-widget', 'abovecontent')
    if get_setting(u'belowcontent_display_type'):
        assign_slot(u'navigation-widget', 'belowcontent')
    if get_setting(u'beforebodyend_display_type'):
        assign_slot(u'navigation-widget', 'beforebodyend')
