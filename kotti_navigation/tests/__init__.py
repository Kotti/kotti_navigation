from kotti.views.slots import assign_slot

from kotti_settings.util import set_setting


def set_nav_setting(slot, setting, value):
    name = 'kotti_navigation-'
    name += "%s_%s" % (slot, setting)
    set_setting(name, value)


def _populate():
    from kotti.testing import _populator
    from kotti_navigation.populate import populate
    _populator()
    populate()


def _populate_left():
    _populate()
    assign_slot('navigation-widget', 'left')


def _populate_right():
    _populate()
    assign_slot('navigation-widget', 'right')
