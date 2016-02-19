from pyramid.i18n import TranslationStringFactory
from logging import getLogger
log = getLogger('kotti_navigation: ')

_ = TranslationStringFactory('kotti_navigation')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_navigation deform_bootstrap js.deform'
    settings['kotti.populators'] += ' kotti_navigation.populate.populate'
    # We override nav.pt.
    settings['kotti.asset_overrides'] += ' kotti_navigation:kotti-overrides/'


def includeme(config):  # pragma: no cover
    config.add_translation_dirs('kotti_navigation:locale')
    config.scan(__name__, ignore='.tests')
