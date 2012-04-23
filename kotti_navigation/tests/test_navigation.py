from pyramid.threadlocal import get_current_registry
# from kotti import get_settings
from kotti.testing import (
    FunctionalTestBase,
    DummyRequest,
)
from kotti.resources import (
        get_root,
        Content,
)
from kotti_navigation import render_navigation_widget


class NavigationDummyRequest(DummyRequest):

    def __init__(self):
        super(NavigationDummyRequest, self).__init__()
        self.context = None

    def static_url(self, name):
        return ''


class TestNavigationWidget(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_navigation.kotti_configure',
                    'kotti_navigation.navigation_widget.include_root': 'true',
                    'kotti_navigation.navigation_widget.open_all': 'false'}
        super(TestNavigationWidget, self).setUp(**settings)

    def test_render_widget(self):
        root = get_root()
        html = render_navigation_widget(root, NavigationDummyRequest())
        assert '<ul class="nav nav-pills nav-stacked">' in html

    def test_include_root(self):
        request = NavigationDummyRequest()
        root = get_root()
        html = render_navigation_widget(root, request)
        assert u'Welcome to Kotti' in html
        get_current_registry().settings['kotti_navigation.navigation_widget.include_root'] = u'false'
        # get_settings()['kotti_navigation.navigation_widget.include_root'] = u'false'
        html = render_navigation_widget(root, request)
        assert u'Welcome to Kotti' not in html

    def test_open_tree(self):
        request = NavigationDummyRequest()
        root = get_root()
        root[u'content_1'] = Content()
        root[u'content_1'][u'sub_1'] = Content()
        root[u'content_2'] = Content()
        root[u'content_2'][u'sub_2'] = Content()

        request.context = root
        html = render_navigation_widget(root, request)
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_1']
        html = render_navigation_widget(root[u'content_1'], request)
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' not in html

        request.context = root[u'content_2']
        html = render_navigation_widget(root[u'content_2'], request)
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        request.context = root[u'content_2'][u'sub_2']
        html = render_navigation_widget(root[u'content_2'][u'sub_2'], request)
        assert u'content_1' in html
        assert u'sub_1' not in html
        assert u'content_2' in html
        assert u'sub_2' in html

        get_current_registry().settings['kotti_navigation.navigation_widget.open_all'] = u'true'
        request.context = root
        html = render_navigation_widget(root, request)
        assert u'content_1' in html
        assert u'sub_1' in html
        assert u'content_2' in html
        assert u'sub_2' in html
