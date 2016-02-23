from pytest import mark

from kotti_navigation.tests import set_nav_setting


class TestOptions:

    @mark.user('admin')
    def test_open_all(self, webtest, kn_content, assign_left):
        set_nav_setting('left', 'show_in_context', 'everywhere')
        set_nav_setting('left', 'display_type', 'tree')
        resp = webtest.get('/')
        assert 'Document 1 1' not in resp.body

        set_nav_setting('left', 'options', ['open_all'])
        resp = webtest.get('/')
        assert 'Document 1 1' in resp.body

    @mark.user('admin')
    def test_hidden_nav_points(self, webtest, kn_content, assign_left):
        set_nav_setting('left', 'options', ['open_all'])
        set_nav_setting('left', 'show_in_context', 'everywhere')
        set_nav_setting('left', 'display_type', 'tree')

        resp = webtest.get('/')
        assert 'Document 1 1' in resp.body

        resp = webtest.get('/document-1/@@contents')
        form = resp.forms[1]
        form.set('children', True)
        resp = form.submit(name='hide').maybe_follow()
        assert 'Document 1 1 is no longer visible' in resp.body

        resp = webtest.get('/')
        assert 'Document 1 1' not in resp.body

        set_nav_setting('left', 'options', ['open_all', 'show_hidden_while_logged_in'])
        resp = webtest.get('/')
        assert 'Document 1 1' in resp.body

    @mark.user('admin')
    def test_include_root(self, webtest, kn_content, assign_left):
        set_nav_setting('left', 'show_in_context', 'everywhere')
        set_nav_setting('left', 'display_type', 'tree')

        resp = webtest.get('/')
        assert 'title="Congratulations! ' not in resp.body

        set_nav_setting('left', 'options', ['include_root'])
        resp = webtest.get('/')
        assert 'title="Congratulations! ' in resp.body

    @mark.user('admin')
    def test_stacked(self, webtest, kn_content, assign_left):
        set_nav_setting('left', 'show_in_context', 'everywhere')
        set_nav_setting('left', 'display_type', 'tree')

        resp = webtest.get('/')
        assert '<ul class="nav nav-pills nav-stacked">' not in resp.body

        set_nav_setting('left', 'options', ['stacked'])
        resp = webtest.get('/')
        assert '<ul class="nav nav-pills nav-stacked">' in resp.body

    @mark.user('admin')
    def test_dropdowns(self, webtest, kn_content, assign_left):
        set_nav_setting('left', 'show_in_context', 'everywhere')
        set_nav_setting('left', 'display_type', 'tree')

        resp = webtest.get('/')
        assert 'Document 1 1' not in resp.body
        assert 'dropdown-submenu' not in resp.body

        set_nav_setting('left', 'options', ['dropdowns'])
        resp = webtest.get('/')
        assert 'Document 1 1' in resp.body
        assert 'dropdown-submenu' in resp.body
