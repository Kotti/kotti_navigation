import colander
import deform
from deform_bootstrap.widget import ChosenMultipleWidget

from kotti import get_settings
from kotti.views.slots import assign_slot

from kotti_settings.util import add_settings
from kotti_settings.util import get_setting
from kotti_grid import _


display_types = ((u'', _(u'Not enabled')),
                 (u'vertical', _(u'Vertical')),
                 (u'horizontal', _(u'Horizontal')),
                 # ('ver_list', _(u'Vertical list')),
                 # ('ver_tabs', _(u'Vertical tabs')),
                 # ('ver_pills', _(u'Vertical pills')),
                 # ('hor_tabs', _(u'Horizontal tabs')),
                 # ('hor_pills', _(u'Horizontal pills')),
                )

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


    #X hor_tabs                     horizontal (items)    context children
    #X hor_pills                    horizontal (items)    context children
    # hor_tabs_with_dropdowns      horizontal (items)    context children +1
    # hor_pills_with_dropdowns     horizontal (items)    context children +1
    # breadcrumbs                  horizontal (items)    path to context
    #C ver_tabs_stacked             vertical (tree-like)  context children
    #C ver_pills_stacked            vertical (tree-like)  context children
    # ver_tabs_stacked_open_all    vertical (tree-like)  entire hierarchy
    # ver_pills_stacked_open_all   vertical (tree-like)  entire hierarchy
    #X ver_list                     vertical (items)      context children
    # menu                         button with caret     path to context +1
    #                              firing dropdown menu


# class SlotEnable(colander.SchemaNode):
#     default = True


class DisplayType(colander.SchemaNode):
    default = u''
    missing = u''
    widget = deform.widget.SelectWidget(values=display_types)


class Label(colander.SchemaNode):
    default = u''
    missing = u''


class Options(colander.SchemaNode):
    widget = ChosenMultipleWidget(values=options)
    default = []
    missing = []


@colander.deferred
def deferred_content_types_widget(node, kw):
    types = get_settings()['kotti.available_types']
    values = [(type_, type_.type_info.name) for type_ in types]
    widget = ChosenMultipleWidget(values=values)
    return widget


class ContentTypes(colander.SchemaNode):
    widget = deferred_content_types_widget
    default = []
    missing = []


class ShowHiddenWhileLoggedIn(colander.SchemaNode):
    default = False
    missing = False


# kotti_navigation.navigation_widget.top_display_type = ver_list
# kotti_navigation.navigation_widget.top_show_menu = true
# kotti_navigation.navigation_widget.top_label = context:
# kotti_navigation.navigation_widget.top_include_root = true
# kotti_navigation.navigation_widget.top_show_hidden_while_logged_in = true
# kotti_navigation.navigation_widget.top_exclude_content_types =
#     kotti.resources.Image


class NavigationSchema(colander.MappingSchema):
    top_display_type = DisplayType(colander.String(),
                             name=u'top_display_type',
                             title=_(u'Top display type'))
    top_options = Options(colander.Set(),
                            name=u'top_options',
                            title=_(u'Top options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    top_exclude = ContentTypes(colander.Set(),
                            name=u'top_exclude',
                            title=_(u'Top exclude Content Types'))
    top_include = ContentTypes(colander.Set(),
                            name=u'top_include',
                            title=_(u'Top include Content Types'))
    top_label = Label(colander.String(),
                             name=u'top_label',
                             title=_(u'Top label'))

    left_display_type = DisplayType(colander.String(),
                             name=u'left_display_type',
                             title=_(u'Left display type'))
    left_options = Options(colander.Set(),
                            name=u'left_options',
                            title=_(u'Left options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    left_exclude = ContentTypes(colander.Set(),
                            name=u'left_exclude',
                            title=_(u'Left exclude Content Types'))
    left_include = ContentTypes(colander.Set(),
                            name=u'left_include',
                            title=_(u'Left include Content Types'))
    left_label = Label(colander.String(),
                             name=u'left_label',
                             title=_(u'Left label'))

    right_display_type = DisplayType(colander.String(),
                             name=u'right_display_type',
                             title=_(u'Right display type'))
    right_options = Options(colander.Set(),
                            name=u'right_options',
                            title=_(u'Right options'),
                            description=_(u'Enable dropdowns feature '
                                          u'only makes sense for horizontal '
                                          u'display type.'))
    right_label = Label(colander.String(),
                             name=u'right_label',
                             title=_(u'Right label'))
    right_exclude = ContentTypes(colander.Set(),
                            name=u'right_exclude',
                            title=_(u'Right exclude Content Types'))
    right_include = ContentTypes(colander.Set(),
                            name=u'right_include',
                            title=_(u'Right include Content Types'))


NavigationSettings = {
    'name': 'navigation_settings',
    'title': _(u'Navigation Settings'),
    'description': _(u"Settings for kotti_navigation"),
    'success_message': _(u"Successfully saved kotti_navigation settings."),
    'schema_factory': NavigationSchema,
}


def populate():
    from kotti.resources import get_root
    root = get_root()
    #del root.annotations['kotti_settings']
    add_settings(NavigationSettings)
    if get_setting(u'left_display_type', None) is not None:
        assign_slot('navigation-widget', 'left')
    if get_setting(u'right_display_type', None) is not None:
        assign_slot('navigation-widget', 'right')
    #if get_setting(u'right_enable', False):
    #    assign_slot('navigation-widget', 'right')
