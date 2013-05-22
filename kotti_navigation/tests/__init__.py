from kotti_settings.util import set_setting


def set_nav_setting(slot, setting, value):
    name = 'kotti_navigation-'
    name += "%s_%s" % (slot, setting)
    set_setting(name, value)
