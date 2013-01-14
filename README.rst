================
kotti_navigation
================

This is an extension to the Kotti CMS that renders a navigation in the
slots for a Kotti website (left, right, abovecontent, etc.).

`Find out more about Kotti`_

Setting up the navigation widget
================================

To set up the navigation widget to display on every page in Kotti in a given
slot (left, right, abovecontent, belowcontent, belowbodyend), instead of
setting a general config in kotti.configurators, set a specific choice in
pyramid.includes in your ini file::

    pyramid.includes = 
        ...
        kotti_navigation.include_navigation_widget_right

.. Note:: Configure navigation for only one slot.

Choices of widget position configuration for pyramid.includes are::

    kotti_navigation.include_navigation_widget_left
    kotti_navigation.include_navigation_widget_right
    kotti_navigation.include_navigation_widget_abovecontent
    kotti_navigation.include_navigation_widget_belowcontent
    kotti_navigation.include_navigation_widget_belowbodyend

To exclude the root of the site from the navigation, set the
``kotti_navigation.navigation_widget.include_root`` variable.::

    kotti_navigation.navigation_widget.include_root = false

To open the whole navigation all the time, set the
``kotti_navigation.navigation_widget.open_all`` variable. This is useful if
you plan to set up a popup menu via css or javascript::

    kotti_navigation.navigation_widget.open_all = false

By default, only the immediate children for the context are shown in the
navigation display, as a simple horizontal list of navpills wrapped within the
available space. This style of display is appropriate for navigation menus in
the abovecontent, belowcontent, and belowbodyend slots. For uses in left and
right slots, and perhaps in other cases, a tree display is preferred. Control
this with the display_as_tree boolean setting (default is False)::

    kotti_navigation.navigation_widget.display_as_tree = true

If using a list display for navigation (display_as_tree = False), the default
will only list children of the current context. This may not provide a clear
user interface, such that it is obvious that the list items are children of
the current context (especially when the abovecontent slot is used). To help,
you can set::

    kotti_navigation.navigation_widget.include_context_label_in_list = true

which will put the context as a label in the first item of the nav list, along
with a colon. If the current context is "Animals" and the children are "Dogs"
and "Cats", the nav list would be: Animals: Dogs Cats, as navpills.

You can exclude specific content types from the whole navigation
structure. If you not want to show images in the navigation at all,
set the ``kotti_navigation.navigation_widget.exclude_content_types`` 
variable to the following.::

    kotti_navigation.navigation_widget.exclude_content_types = 
        kotti.resources.Image
        kotti_myaddon.resources.MyContentType


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
