from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from kotti.fanstatic import view_css


library = Library('kotti_navigation', 'static')

style = Resource(
    library,
    'css/style.css',
    minified='css/style.min.css'
)

dropdown = Resource(
    library,
    'css/dropdown.css',
    depends=[view_css],
    minified='css/dropdown.min.css'
)


kotti_navigation = Group([style, ])
kotti_navigation_dropdown = Group([dropdown, ])
