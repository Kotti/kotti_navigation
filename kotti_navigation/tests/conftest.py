from pytest import fixture
from pytest import mark

from kotti.views.slots import assign_slot

pytest_plugins = "kotti"


@fixture(scope='session')
def custom_settings():
    return {
        'kotti.configurators': 'kotti_navigation.kotti_configure'
        }

@fixture
def kn_populate(db_session):
    from kotti_navigation.populate import populate
    populate()


@mark.user('admin')
@fixture
def kn_content(webtest, kn_populate, root, workflow):

    from kotti.workflow import get_workflow

    resp = webtest.get('/add_document')
    form = resp.forms['deform']
    form['title'].value = 'Document 1'
    form['description'].value = 'This is the first document'
    resp = form.submit('save')

    resp = webtest.get('/document-1/add_document')
    form = resp.forms['deform']
    form['title'].value = 'Document 1 1'
    form['description'].value = 'This is the second document'
    resp = form.submit('save')

    wf = get_workflow(root['document-1']);
    wf.transition_to_state(root['document-1'], None, u'public')
    wf = get_workflow(root['document-1']['document-1-1']);
    wf.transition_to_state(root['document-1']['document-1-1'], None, u'public')


@fixture
def assign_left():
    assign_slot('navigation-widget', 'left')


@fixture
def assign_right():
    assign_slot('navigation-widget', 'right')


def settings():
    from kotti import _resolve_dotted
    from kotti import conf_defaults
    settings = conf_defaults.copy()
    settings['kotti.secret'] = 'secret'
    settings['kotti.secret2'] = 'secret2'
    settings['kotti.configurators'] += \
        ' kotti_settings.kotti_configure kotti_navigation.kotti_configure'
    settings['kotti.populators'] += ' kotti_navigation.populate.populate kotti_navigation.tests._populate_left'
    settings['pyramid.includes'] += ' kotti_settings kotti_settings.views'
    settings = _resolve_dotted(settings)
    return settings


def setup_app():
    from kotti import base_configure
    import ipdb;ipdb.set_trace()
    return base_configure({}, **settings()).make_wsgi_app()


@fixture
def kn_setup():
    setup_app()


@fixture
def kn_request(dummy_request):
    setattr(dummy_request, 'kotti_slot', 'left')
    return dummy_request
