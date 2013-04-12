from pyramid.threadlocal import get_current_registry

from kotti.testing import FunctionalTestBase
from kotti.testing import DummyRequest

from kotti.resources import get_root
from kotti.resources import Content

from kotti.views.util import render_view

from kotti_navigation.views import navigation_widget_items
from kotti_navigation.views import navigation_widget_tree
from kotti_navigation.views import is_node_open


class NavigationDummyRequest(DummyRequest):

    # The path param is added here, because the nav display view names contain
    # the location, e.g., '/context/navigation-menu-left', and this is how the
    # associated render function in python gets the location. It will work in
    # testing if path is set to only 'top', 'left', etc.
    def __init__(self, context=None, path='/some-navigation-widget-left'):
        super(NavigationDummyRequest, self).__init__()
        self.context = context
        self.path = path

    def static_url(self, name):
        return ''  # pragma: no cover


class TestNavigationWidgetAsHorPills(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
            'kotti_navigation.navigation_widget.left_display_type': 'hor_pills',
            'kotti_navigation.navigation_widget.left_show_menu': 'true',
            'kotti_navigation.navigation_widget.left_label': 'context'}
        super(TestNavigationWidgetAsHorPills, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_view(root, NavigationDummyRequest(path='/some-navigation-widget-left'),
                           name='navigation-widget-items-left')
        assert ' class="nav nav-pills"' in html

    def test_show_dropdown_menus(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()
        result = navigation_widget_items(root, request)

        c1 = root[u'content_1'] = Content(title=u'Content_1')
        c1[u'sub_1'] = Content(title=u'Sub_1')
        c1[u'sub_1'][u'sub_sub_1'] = Content(title=u'Sub_Sub_1')
        c2 = root[u'content_2'] = Content(title=u'Content_2')
        c2[u'sub_2'] = Content(title=u'Sub_2')

        html = render_view(c1, NavigationDummyRequest(path='/some-navigation-widget-left'),
                           name='navigation-widget-items-left')

        assert not u'nav-list-careted' in html

        st = get_current_registry().settings
        st['kotti_navigation.navigation_widget.left_display_type'] = u'hor_pills_with_dropdowns'

        html = render_view(c1, NavigationDummyRequest(path='/some-navigation-widget-left'),
                           name='navigation-widget-items-left')

        assert u'nav-list-careted' in html

    def test_label(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        result = navigation_widget_items(root, request)

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items in [context] are:'
        result = navigation_widget_items(root[u'content_1'], request)
        assert result['label'] == 'Items in [Content_1] are:'

        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items are:'
        result = navigation_widget_items(root[u'content_1'], request)
        assert result['label'] == 'Items are:'


class TestNavigationWidgetAsTree(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.left_display_type': 'ver_tabs_stacked',
                    'kotti_navigation.navigation_widget.left_include_root': 'true',
                    'kotti_navigation.navigation_widget.left_label': 'none'}
        super(TestNavigationWidgetAsTree, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_view(root, NavigationDummyRequest(path='/some-navigation-widget-left'),
                           name='navigation-widget-tree-left')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

    def test_include_root(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()
        result = navigation_widget_tree(root, request)
        assert result['include_root'] == True
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_include_root'] = u'false'
        result = navigation_widget_tree(root, request)
        assert result['include_root'] == False

    def test_display_type(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()
        result = navigation_widget_tree(root, request)
        assert result['display_type'] == 'ver_tabs_stacked'
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_display_type'] = u'hor_tabs'
        result = navigation_widget_tree(root, request)
        assert result['display_type'] == 'hor_tabs'

    def test_is_tree_open(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()
        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        request.context = root
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_2']
        html = render_view(root[u'content_2'], request,
                           name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        request.context = root[u'content_2'][u'sub_2']
        html = render_view(root[u'content_2'][u'sub_2'], request,
                           name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_display_type'] = u'ver_tabs_stacked_open_all'
        request.context = root
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' in html

    def test_is_node_open(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()
        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        request.context = root
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert is_node_open(root, request)
        assert is_node_open(root['content_1'], request) == False
        assert is_node_open(root['content_2'], request) == False

        # We do not check against open_all, because the page template checks
        # tree_is_open_all before calling is_node_open(), which assumes that
        # tree_is_open_all is False, and nodes must be checked individually.


    def test_show_hidden(self):
        root = get_root()
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # with standard settings the hidden nav items are hidden
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'content_2' not in html

        # if we change the setting, the nav items still hidden
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_show_hidden_while_logged_in'] =\
            u'true'
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'content_2' not in html

        # we have to be logged in to see the navitem
        # BUT how is this possible???
        # from kotti.views.login import login
        # request.params['submit'] = u'on'
        # request.params['login'] = u'admin'
        # request.params['password'] = u'secret'
        # request.params['HTTP_HOST'] = u'babbelhorst.net'
        # result = self.login()
        # html = render_navigation_widget(root, request)
        # assert u'content_1' in html
        # assert u'content_2' in html

    def test_include_content_types(self):
        root = get_root()
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # If we include the content type the nav item is present.
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_include_content_types'] =\
            u'kotti.resources.Content'
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html

        # With an empty include_content_types, the nav item is not present.
        se['kotti_navigation.navigation_widget.left_include_content_types'] =\
            u''
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html

        # Again, with show_hidden True.
        # [TODO] See comment above about the need to log in for testing this.
        #se['kotti_navigation.navigation_widget.left_show_hidden_while_logged_in'] =\
        #    u'true'
        #se['kotti_navigation.navigation_widget.left_include_content_types'] =\
        #    u'kotti.resources.Content'
        #assert u'content_1' in html
        #assert u'content_2' in html

    def test_exclude_content_types(self):
        root = get_root()
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root[u'content_1'] = Content()

        # with no exclude the hidden nav items is shown
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html

        # if we exclude the content type the nav item disappears
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_exclude_content_types'] =\
            u'kotti.resources.Content'
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' not in html


class TestNavigationWidgetAllLocations(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.top_display_type': 'hor_pills_with_dropdowns',
                    'kotti_navigation.navigation_widget.top_show_menu': 'true',
                    'kotti_navigation.navigation_widget.top_label': 'context:',
                    'kotti_navigation.navigation_widget.top_include_root': 'false',
                    'kotti_navigation.navigation_widget.top_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.top_exclude_content_types': 'kotti.resources.Image',
                    'kotti_navigation.navigation_widget.abovecontent_display_type': 'ver_tabs_stacked_open_all',
                    'kotti_navigation.navigation_widget.abovecontent_show_menu': 'false',
                    'kotti_navigation.navigation_widget.abovecontent_include_root': 'true',
                    'kotti_navigation.navigation_widget.abovecontent_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.abovecontent_exclude_content_types': 'kotti.resources.Image',
                    'kotti_navigation.navigation_widget.left_display_type': 'hor_tabs_with_dropdowns',
                    'kotti_navigation.navigation_widget.left_show_menu': 'true',
                    'kotti_navigation.navigation_widget.left_include_root': 'true',
                    'kotti_navigation.navigation_widget.left_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.left_exclude_content_types': 'kotti.resources.Image',
                    'kotti_navigation.navigation_widget.right_display_type': 'ver_pills_stacked',
                    'kotti_navigation.navigation_widget.right_show_menu': 'false',
                    'kotti_navigation.navigation_widget.right_label': 'Images:',
                    'kotti_navigation.navigation_widget.right_include_root': 'false',
                    'kotti_navigation.navigation_widget.right_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.right_include_content_types': 'kotti.resources.Image',
                    'kotti_navigation.navigation_widget.belowcontent_display_type': 'menu',
                    'kotti_navigation.navigation_widget.belowcontent_show_menu': 'true',
                    'kotti_navigation.navigation_widget.belowcontent_include_root': 'true',
                    'kotti_navigation.navigation_widget.belowcontent_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.belowcontent_exclude_content_types': 'kotti.resources.Image',
                    'kotti_navigation.navigation_widget.beforebodyend_display_type': 'breadcrumbs',
                    'kotti_navigation.navigation_widget.beforebodyend_label': 'You are here:',
                    'kotti_navigation.navigation_widget.beforebodyend_show_hidden_while_logged_in': 'true',
                    'kotti_navigation.navigation_widget.beforebodyend_exclude_content_types': 'kotti.resources.Image'}
        super(TestNavigationWidgetAllLocations, self).setUp(**settings)

    def test_label(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-left')
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        result = navigation_widget_items(root, request)

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items in [context] are:'
        result = navigation_widget_items(root[u'content_1'], request)
        assert result['label'] == 'Items in [Content_1] are:'

class TestNavigationWidgetAsTreeInTop(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.top_display_type': 'ver_tabs_stacked',
                    'kotti_navigation.navigation_widget.top_include_root': 'true',
                    'kotti_navigation.navigation_widget.top_label': 'none'}
        super(TestNavigationWidgetAsTreeInTop, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_view(root, NavigationDummyRequest(path='/some-navigation-widget-top'),
                           name='navigation-widget-tree-top')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

class TestNavigationWidgetAsMenuInTop(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.top_display_type': 'menu',
                    'kotti_navigation.navigation_widget.top_include_root': 'true',
                    'kotti_navigation.navigation_widget.top_include_content_types': 'kotti.resources.Content',
                    'kotti_navigation.navigation_widget.top_label': 'none'}
        super(TestNavigationWidgetAsMenuInTop, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-top')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-menu-top')
        assert '<ul class="nav nav-list">' in html

class TestNavigationWidgetAsTreeInRight(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.right_display_type': 'ver_tabs_stacked_open_all',
                    'kotti_navigation.navigation_widget.right_include_root': 'true',
                    'kotti_navigation.navigation_widget.right_include_content_types': 'kotti.resources.Content',
                    'kotti_navigation.navigation_widget.right_label': 'Only Content Shows Here'}
        super(TestNavigationWidgetAsTreeInRight, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-right')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-tree-right')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

class TestNavigationWidgetAsTreeInAbovecontent(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.abovecontent_display_type': 'ver_tabs_stacked_open_all',
                    'kotti_navigation.navigation_widget.abovecontent_include_root': 'true',
                    'kotti_navigation.navigation_widget.abovecontent_include_content_types': 'kotti.resources.Content',
                    'kotti_navigation.navigation_widget.abovecontent_label': 'Only Content Shows Here'}
        super(TestNavigationWidgetAsTreeInAbovecontent, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-abovecontent')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-tree-abovecontent')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

class TestNavigationWidgetAsTreeInBelowcontent(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.belowcontent_display_type': 'ver_tabs_stacked_open_all',
                    'kotti_navigation.navigation_widget.belowcontent_include_root': 'true',
                    'kotti_navigation.navigation_widget.belowcontent_include_content_types': 'kotti.resources.Content',
                    'kotti_navigation.navigation_widget.belowcontent_label': 'Only Content Shows Here'}
        super(TestNavigationWidgetAsTreeInBelowcontent, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-belowcontent')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-tree-belowcontent')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

class TestNavigationWidgetAsTreeInBeforebodyend(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.beforebodyend_display_type': 'ver_tabs_stacked_open_all',
                    'kotti_navigation.navigation_widget.beforebodyend_include_root': 'true',
                    'kotti_navigation.navigation_widget.beforebodyend_include_content_types': 'kotti.resources.Content',
                    'kotti_navigation.navigation_widget.beforebodyend_label': 'Only Content Shows Here'}
        super(TestNavigationWidgetAsTreeInBeforebodyend, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-beforebodyend')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        request.context = root[u'content_1']
        html = render_view(root[u'content_1'], request,
                           name='navigation-widget-tree-beforebodyend')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

class TestNavigationWidgetAsBreadcrumbsInBeforebodyend(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.beforebodyend_display_type': 'breadcrumbs',
                    'kotti_navigation.navigation_widget.beforebodyend_include_root': 'true',
                    'kotti_navigation.navigation_widget.beforebodyend_label': 'You are here:'}
        super(TestNavigationWidgetAsBreadcrumbsInBeforebodyend, self).setUp(**settings)

    def test_render_widget(self):
        request = NavigationDummyRequest(path='/some-navigation-widget-beforebodyend')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        request.context = root[u'content_1'][u'sub_1']
        html = render_view(root[u'content_1'][u'sub_1'], request,
                           name='navigation-widget-breadcrumbs-beforebodyend')
        assert 'You are here:' in html

