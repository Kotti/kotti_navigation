from pyramid.threadlocal import get_current_registry
from kotti.testing import (
    FunctionalTestBase,
    DummyRequest,
)
from kotti.resources import (
        get_root,
        Content,
)
from kotti.views.util import render_view
from kotti_navigation.views import navigation_widget_items
from kotti_navigation.views import navigation_widget_tree


class NavigationDummyRequest(DummyRequest):

    def __init__(self, context=None):
        super(NavigationDummyRequest, self).__init__()
        self.context = context

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
        html = render_view(root, NavigationDummyRequest(),
                           name='navigation-widget-items-left')
        assert ' class="nav nav-pills"' in html

    def test_show_dropdown_menus(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget_items(root, request, location='left')

        c1 = root[u'content_1'] = Content(title=u'Content_1')
        c1[u'sub_1'] = Content(title=u'Sub_1')
        c1[u'sub_1'][u'sub_sub_1'] = Content(title=u'Sub_Sub_1')
        c2 = root[u'content_2'] = Content(title=u'Content_2')
        c2[u'sub_2'] = Content(title=u'Sub_2')

        html = render_view(c1, NavigationDummyRequest(),
                           name='navigation-widget-items-left')

        assert not u'nav-list-careted' in html

        st = get_current_registry().settings
        st['kotti_navigation.navigation_widget.left_display_type'] = u'hor_pills_with_dropdowns'

        html = render_view(c1, NavigationDummyRequest(),
                           name='navigation-widget-items-left')

        assert u'nav-list-careted' in html

    def test_label(self):
        request = NavigationDummyRequest()
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        result = navigation_widget_items(root, request, location='left')

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items in [context] are:'
        result = navigation_widget_items(root[u'content_1'], request, location='left')
        assert result['label'] == 'Items in [Content_1] are:'

        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items are:'
        result = navigation_widget_items(root[u'content_1'], request, location='left')
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
        html = render_view(root, NavigationDummyRequest(),
                           name='navigation-widget-tree-left')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

    def test_include_root(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget_tree(root, request, location='left')
        assert result['include_root'] == True
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_include_root'] = u'false'
        result = navigation_widget_tree(root, request, location='left')
        assert result['include_root'] == False

    def test_display_type(self):
        request = NavigationDummyRequest()
        root = get_root()
        result = navigation_widget_tree(root, request, location='left')
        assert result['display_type'] == 'ver_tabs_stacked'
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_display_type'] = u'hor_tabs'
        result = navigation_widget_tree(root, request, location='left')
        assert result['display_type'] == 'hor_tabs'

    def test_is_tree_open(self):
        request = NavigationDummyRequest()
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
        assert u'content_2' not in html
        assert u'sub_2' not in html

        request.context = root[u'content_2']
        html = render_view(root[u'content_2'], request,
                           name='navigation-widget-tree-left')
        assert u'content_1' not in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        request.context = root[u'content_2'][u'sub_2']
        html = render_view(root[u'content_2'][u'sub_2'], request,
                           name='navigation-widget-tree-left')
        assert u'content_1' not in html
        assert u'sub_1' not in html
        assert u'content_2' not in html
        assert u'sub_2' not in html

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_display_type'] = u'ver_tabs_stacked_open_all'
        request.context = root
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' in html

    def test_show_hidden(self):
        root = get_root()
        request = DummyRequest()
        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # with standard settings the hidden nav points are hidden
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'content_2' not in html

        # if we change the setting, the nav points still hidden
        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_show_hidden_while_logged_in'] =\
            u'true'
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html
        assert u'content_2' not in html

        # we have to be logged in to see the navpoint
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

    def test_exclude_content_types(self):
        root = get_root()
        request = DummyRequest()
        root[u'content_1'] = Content()

        # with no exclude the hidden nav points is shown
        html = render_view(root, request, name='navigation-widget-tree-left')
        assert u'content_1' in html

        # if we exclude the content type the nav point disappears
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
        request = NavigationDummyRequest()
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        result = navigation_widget_items(root, request, location='left')

        se = get_current_registry().settings
        se['kotti_navigation.navigation_widget.left_label'] =\
            u'Items in [context] are:'
        result = navigation_widget_items(root[u'content_1'], request, location='left')
        assert result['label'] == 'Items in [Content_1] are:'
