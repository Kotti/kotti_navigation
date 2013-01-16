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

Here are the slots available for the navigation widget::

    +------------------------------------------------------+
    | nav (the nav in the Kotti toolbar                    |
    |------------------------------------------------------|
    | editor_bar                                           |
    |+----------------------------------------------------+|
    || breadcrumbs                                        ||
    |+-------------++---------------------++--------------+|
    || SLOT "left" || SLOT "abovecontent" || SLOT "right" ||
    ||             |+---------------------+|              ||
    ||             || Content             ||              ||
    ||             |+---------------------+|              ||
    ||             || SLOT "belowcontent" ||              ||
    |+-------------++---------------------++--------------+|
    | footer                                               |
    |------------------------------------------------------|
    | SLOT "beforebodyend"                                 |
    +------------------------------------------------------+

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
this with the display_type setting, which can be either ``horizontal`` or
``tree`` (default is horizontal)::

    kotti_navigation.navigation_widget.display_type = horizontal

If using a horizontal list display for navigation, the default will list
children of the current context in a horizontal list of nav pills that wrap, if
necessary. Along with the toolbar and and breadcrumbs, this may provide a
perfectly good nav display. When the abovecontent slot is used, however, the
title for the context is _underneath_ the nav list, so it may not be clear
enough that that the nav pill items are contained within the context.  Perhaps
this would be true for the left slot, as well, but a bare nav pill list in the
right and belowcontent slots might work well Regardless, for any slot, if
desired, set label (default is none) to a string as illustrated in the
following examples.

For each example, the context is assumed to be a document titled Animals, and
there are two children titled Dogs and Cats, the horizontal nav pill list will
have items as Animals: Dogs Cats.

If label is not set, the default value of none will result in two nav pill li
items, <Dogs> and <Cats> (< > notation used here to denote nav pill li items).

Using a custom sring, punctuated with a colon::

    kotti_navigation.label = Contained Items

would result in a nav-header styled label with two nav pill li items, as::

    Contained items <Dogs> <Cats>

Using punctuation might be a good idea::

    kotti_navigation.label = Subitems:

would result in a nav-header styled label with two nav pill li items, as::

    Subitems: <Dogs> <Cats>

or, perhaps with some other punctuation::

    kotti_navigation.label = Contents >>

etc.

Option 2, set label to a string using the word ``context`` anywhere in the
string as a placeholder for context.title. If the label is set to be only
the word ``context`` (only the word, with no punctuation), then a nav pill
will be used for the label::

    kotti_navigation.label = context

The result would be three nav pill li items, as::

    <Animals> <Dogs> <Cats>

with <Animals> as the active link.

With any punctuation or additional text of any sort, as with::

    label = context:

then instead of a nav pill, a nav-header styled li is used::

    Animals: <Dogs> <Cats>

If a phrase is used, take care to word appropriately, perhaps aided by use of
quotes or another indicator for context, such as (), [], etc.::

    kotti_navigation.label = Items in [context] are:::

would result in::

    Items in [Animals] are: <Dogs> <Cats>

and::

    kotti_navigation.label = "context" contains:

would result in::

    "Animals" contains: <Dogs> <Cats>

etc.

.. Note:: String params in ini config files do not have quotes, so the string
          is whatever comes after the = sign, with leading whitespace deleted.

Excluding Content Types
-----------------------

You can exclude specific content types from the whole navigation
structure. If you not want to show images in the navigation at all,
set the ``kotti_navigation.navigation_widget.exclude_content_types`` 
variable to the following.::

    kotti_navigation.navigation_widget.exclude_content_types = 
        kotti.resources.Image
        kotti_myaddon.resources.MyContentType


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
