================
kotti_navigation
================

This is an extension to the Kotti CMS that renders a navigation in the
left or right slot.

`Find out more about Kotti`_

Setting up the navigation widget
================================

To set up the navigation widget to display on every page in Kotti on the
left side add ``kotti_navigation.kotti_configure`` to the
``kotti.configurators`` setting in your ini file::

    kotti.configurators = kotti_navigation.kotti_configure

To set up the navigation widget on the right side you have to use the
pyramid.includes option in your ini file::

    pyramid.includes = 
        ...
        kotti_navigation.include_navigation_widget_right

To exclude the root of the site from the navigation, set the
``kotti_navigation.navigation_widget.include_root`` variable.::

    kotti.configurators = kotti_navigation.kotti_configure
    kotti_navigation.navigation_widget.include_root = false

To open the whole navigation all the time, set the
``kotti_navigation.navigation_widget.open_all`` variable. This is useful if
you plan to set up a popup menu via css or javascript::

    kotti.configurators = kotti_navigation.kotti_configure
    kotti_navigation.navigation_widget.open_all = false


You can exclude specific content types from the whole navigation
structure. If you not want to show images in the navigation at all,
set the ``kotti_navigation.navigation_widget.exclude_content_types`` 
variable to the following.::

    kotti_navigation.navigation_widget.exclude_content_types = 
        kotti.resources.Image


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
