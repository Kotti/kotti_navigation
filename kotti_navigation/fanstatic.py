from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource


library = Library('kotti_navigation', 'static')

css = Resource(
    library,
    'css/style.css',
    minified='css/style.min.css'
)

kotti_navigation = Group([css, ])
