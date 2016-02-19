from mock import patch
import pytest

from kotti.resources import get_root
from kotti.resources import Content
from kotti.testing import FunctionalTestBase
from kotti.testing import DummyRequest
from kotti.views.util import render_view

from kotti_navigation.tests import set_nav_setting
from kotti_navigation.util import is_node_open
from kotti_navigation.views import Navigation


class NavigationDummyRequest(DummyRequest):

    # The path param is added here, because the nav display view names contain
    # the location, e.g., '/context/navigation-menu-left', and this is how the
    # associated render function in python gets the location. It will work in
    # testing if path is set to only 'top', 'left', etc.
    def __init__(self, context=None, path='', slot='left'):
        super(NavigationDummyRequest, self).__init__()
        self.context = context
        self.path = path
        self.kotti_slot = slot

    def static_url(self, name):
        return ''  # pragma: no cover


class TestNavigationWidget:

    def test_navigation_widget_no_view(kn_populate, db_session,
                                       dummy_request, events):
        from pyramid.exceptions import PredicateMismatch
        root = get_root()
        navigation = Navigation(root, dummy_request)
        with pytest.raises(PredicateMismatch):
            navigation.navigation_widget()

    def test_navigation_widget_tree(kn_populate, db_session,
                                    kn_request, events):
        from types import FunctionType
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', ['pills'])
        set_nav_setting('left', 'label', u'')
        navigation = Navigation(root, kn_request)
        values = navigation.navigation_widget_tree()

        assert values['display_type'] is 'tree'
        assert values['tree_is_open_all'] is False
        assert values['use_container_class'] is False
        assert values['nav_class'] == 'nav nav-pills'
        assert values['items'] == []
        assert values['label'] == u''
        assert values['location'] is 'left'
        assert type(values['is_node_open']) == FunctionType
        assert values['include_root'] is False
        assert values['show_menu'] is False
        assert values['root'] == root


class NavigationFunctionalTestBase(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure'}
        self.request = NavigationDummyRequest(slot='left')
        super(NavigationFunctionalTestBase, self).setUp(**settings)


class TestNavigationWidgetViews(NavigationFunctionalTestBase):

    def test_render_widget(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'display_manner', 'tabs')
        html = render_view(root, self.request, name='navigation-widget-items')
        assert ' class="nav nav-tabs"' in html

    def test_show_dropdown_menus(self):
        root = get_root()

        c1 = root[u'content_1'] = Content(title=u'Content_1')
        c1[u'sub_1'] = Content(title=u'Sub_1')
        c1[u'sub_1'][u'sub_sub_1'] = Content(title=u'Sub_Sub_1')
        c2 = root[u'content_2'] = Content(title=u'Content_2')
        c2[u'sub_2'] = Content(title=u'Sub_2')

        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', [])
        html = render_view(c1, self.request, name='navigation-widget-items')

        assert u'nav-list-careted' not in html

        set_nav_setting('left', 'display_type', 'items')
        set_nav_setting('left', 'options', ['pills', 'dropdowns'])
        html = render_view(c1, self.request, name='navigation-widget-items')

        assert u'nav-list-careted' in html

    def test_label(self):
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        set_nav_setting('left', 'display_type', 'items')
        set_nav_setting('left', 'options', [])
        set_nav_setting('left', 'label', 'Items in [context] are:')
        navigation = Navigation(root[u'content_1'], self.request)
        result = navigation.navigation_widget_items()
        assert result['label'] == 'Items in [Content_1] are:'

        set_nav_setting('left', 'label', 'Items are:')
        result = navigation.navigation_widget_items()
        assert result['label'] == 'Items are:'


class TestNavigationWidgetTreeView(NavigationFunctionalTestBase):

    def test_render_widget(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'display_manner', 'tabs')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert '<ul class="nav nav-tabs nav-stacked">' in html

    def test_include_root(self):
        root = get_root()

        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'display_manner', 'tabs')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])
        navigation = Navigation(root, self.request)
        result = navigation.navigation_widget_tree()
        assert result['include_root'] == True

        set_nav_setting('left', 'options', ['tabs', 'stacked'])
        result = navigation.navigation_widget_tree()
        assert result['include_root'] == False

    def test_display_type(self):
        root = get_root()

        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'display_manner', 'tabs')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])
        navigation = Navigation(root, self.request)
        result = navigation.navigation_widget_tree()

        assert result['display_type'] == 'tree'
        assert result['nav_class'] == 'nav nav-tabs nav-stacked'

        set_nav_setting('left', 'display_type', 'items')
        result = navigation.navigation_widget_tree()
        assert result['display_type'] == 'items'

    def test_is_tree_open(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])

        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        self.request.context = root
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        self.request.context = root[u'content_1']
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        self.request.context = root[u'content_2']
        html = render_view(root[u'content_2'], self.request,
                           name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        self.request.context = root[u'content_2'][u'sub_2']
        html = render_view(root[u'content_2'][u'sub_2'], self.request,
                           name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        set_nav_setting('left', 'options', ['stacked', 'open_all'])
        self.request.context = root
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' in html

    def test_is_node_open(self):
        root = get_root()

        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        self.request.context = root
        assert is_node_open(root, self.request)
        assert is_node_open(root['content_1'], self.request) == False
        assert is_node_open(root['content_2'], self.request) == False

        # We do not check against open_all, because the page template checks
        # tree_is_open_all before calling is_node_open(), which assumes that
        # tree_is_open_all is False, and nodes must be checked individually.

    def test_show_hidden(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])

        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # with standard settings the hidden nav items are hidden
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'content_2' not in html

        # if we change the setting, the nav items still hidden
        set_nav_setting('left', 'options', ['tabs', 'stacked', 'include_root',
                                            'show_hidden_while_logged_in'])
        with patch('kotti_navigation.util.the_user', return_value='admin'):
            html = render_view(root, self.request,
                               name='navigation-widget-tree')
            assert u'content_1' in html
            assert u'content_2' in html

    def test_include_content_types(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])

        root[u'content_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'].in_navigation = False

        # If we include the content type the nav item is present.
        set_nav_setting('left', 'include', [Content.type_info.name])
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'content_2' not in html

        # With an empty include_content_types, the nav item is not present.
        set_nav_setting('left', 'include', [])
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html
        assert u'content_2' not in html

        # Again, with show_hidden True.
        set_nav_setting('left', 'options', ['stacked', 'include_root',
                                            'show_hidden_while_logged_in'])
        with patch('kotti_navigation.util.the_user', return_value='admin'):
            html = render_view(root, self.request,
                               name='navigation-widget-tree')
            assert u'content_1' in html
            assert u'content_2' in html

    def test_exclude_content_types(self):
        root = get_root()
        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', ['stacked', 'include_root'])

        root[u'content_1'] = Content()

        # with no exclude the hidden nav items is shown
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' in html

        # if we exclude the content type the nav item disappears
        set_nav_setting('left', 'exclude', [Content.type_info.name])
        html = render_view(root, self.request, name='navigation-widget-tree')
        assert u'content_1' not in html


class TestNavigationWidgetAllLocations(NavigationFunctionalTestBase):

    def test_label(self):
        root = get_root()

        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        root[u'content_2'] = Content(title=u'Content_2')
        root[u'content_2'][u'sub_2'] = Content(title=u'Sub_2')

        set_nav_setting('left', 'display_type', 'tree')
        set_nav_setting('left', 'options', [])
        set_nav_setting('left', 'label', 'Items in [context] are:')
        navigation = Navigation(root[u'content_1'], self.request)
        result = navigation.navigation_widget_items()
        assert result['label'] == 'Items in [Content_1] are:'


class TestNavigationWidgetAsTreeInTop(NavigationFunctionalTestBase):

    def test_render_widget(self):
        root = get_root()
        self.request = NavigationDummyRequest(slot='top')
        set_nav_setting('top', 'options', ['stacked', 'include_root'])
        html = render_view(root, self.request,
                           name='navigation-widget-tree')
        assert '<ul class="nav nav-pills nav-stacked">' in html


class TestNavigationWidgetAsMenuInTop(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='top')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        self.request.context = root[u'content_1']
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-menu')
        assert '<ul class="nav nav-list">' in html


class TestNavigationWidgetAsTreeInRight(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='right')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        self.request.context = root[u'content_1']
        set_nav_setting('right', 'display_type', 'tree')
        set_nav_setting('right', 'display_manner', 'pills')
        set_nav_setting('right', 'options', ['stacked', 'include_root',
                                             'open_all'])
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-tree')
        assert '<ul class="nav nav-pills nav-stacked">' in html


class TestNavigationWidgetAsTreeInAbovecontent(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='abovecontent')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        self.request.context = root[u'content_1']
        set_nav_setting('abovecontent', 'display_type', 'tree')
        set_nav_setting('abovecontent', 'options',
                        ['stacked', 'include_root', 'open_all'])
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-tree')
        assert '<ul class="nav nav-pills nav-stacked">' in html


class TestNavigationWidgetAsTreeInBelowcontent(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='belowcontent')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        self.request.context = root[u'content_1']
        set_nav_setting('belowcontent', 'display_type', 'tree')
        set_nav_setting('belowcontent', 'display_manner', 'tabs')
        set_nav_setting('belowcontent', 'options',
                        ['tabs', 'stacked', 'include_root', 'open_all'])
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-tree')
        assert '<ul class="nav nav-tabs nav-stacked">' in html


class TestNavigationWidgetAsTreeInBeforebodyend(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='beforebodyend')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        self.request.context = root[u'content_1']
        set_nav_setting('beforebodyend', 'display_type', 'tree')
        set_nav_setting('beforebodyend', 'options',
                        ['stacked', 'include_root', 'open_all'])
        html = render_view(root[u'content_1'], self.request,
                           name='navigation-widget-tree')
        assert '<ul class="nav nav-pills nav-stacked">' in html


class TestBreadcrumbsInBeforebodyend(NavigationFunctionalTestBase):

    def test_render_widget(self):
        self.request = NavigationDummyRequest(slot='beforebodyend')
        root = get_root()
        root[u'content_1'] = Content(title=u'Content_1')
        root[u'content_1'][u'sub_1'] = Content(title=u'Sub_1')
        self.request.context = root[u'content_1'][u'sub_1']
        set_nav_setting('beforebodyend', 'display_type', 'breadcrumbs')
        set_nav_setting('beforebodyend', 'show_in_context', 'everywhere')
        set_nav_setting('beforebodyend', 'options', ['include_root'])
        set_nav_setting('beforebodyend', 'label', 'You are here:')
        html = render_view(root[u'content_1'][u'sub_1'], self.request,
                           name='navigation-widget')
        assert 'You are here:' in html
