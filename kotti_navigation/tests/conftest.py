from pytest import fixture

pytest_plugins = "kotti"


def settings():
    from kotti import _resolve_dotted
    from kotti import conf_defaults
    settings = conf_defaults.copy()
    settings['kotti.secret'] = 'secret'
    settings['kotti.secret2'] = 'secret2'
    settings['kotti.configurators'] = \
        'kotti_navigation.kotti_configure kotti_settings.kotti_configure'
    settings['kotti.populators'] = 'kotti.testing._populator'
    _resolve_dotted(settings)
    return settings


def setup_app():
    from kotti import base_configure
    return base_configure({}, **settings()).make_wsgi_app()


@fixture
def kn_populate(db_session):
    from kotti_navigation.populate import populate
    populate()


@fixture
def kn_setup():
    setup_app()
