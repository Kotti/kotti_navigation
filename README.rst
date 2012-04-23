================
kotti_navigation
================

This is an extension to the Kotti CMS that renders a navigation in the
left or right slot.

`Find out more about Kotti`_

Setting up the navigation widget
================================

To set up the navigation widget to display on every page in Kotti on the
left hand side, add ``kotti_navigation.kotti_configure`` to the
``kotti.configurators`` setting in your Paste Deploy config::

  kotti.configurators = kotti_navigation.kotti_configure

To exclude the root of the site from the navigation, set the
``kotti_navigation.navigation_widget.include_root`` variable.::

  kotti.configurators = kotti_navigation.kotti_configure
  kotti_navigation.navigation_widget.include_root = false

To open the whole navigation all the time, set the
``kotti_navigation.navigation_widget.open_all`` variable. This might
be useful for a popup menu::
  kotti.configurators = kotti_navigation.kotti_configure
  kotti_navigation.navigation_widget.open_all = false
