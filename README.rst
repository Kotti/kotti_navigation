================
kotti_navigation
================

This is an extension to the Kotti CMS that renders a navigation in one of the
available slots for a Kotti website (left, right, abovecontent, etc.).

`Find out more about Kotti`_

Setting up the navigation widget
================================

These are the configuration settings we will be discussing here for the
navigation widget:::

    # general navigation widget settings, showing defaults
    kotti_navigation.navigation_widget.display_type = tree
    kotti_navigation.navigation_widget.show_context_menu = false
    kotti_navigation.navigation_widget.label = none
    kotti_navigation.navigation_widget.slot = left
    kotti_navigation.navigation_widget.open_all = false
    kotti_navigation.navigation_widget.show_hidden_while_logged_in = true
    kotti_navigation.navigation_widget.exclude_content_types = (e.g., Image)
    kotti_navigation.navigation_widget.include_root = true
     
    # specific to list display
    kotti_navigation.navigation_widget.show_dropdown_menus = true

To set up the navigation widget to display on every page in Kotti in the
default left slot as a tree display, add an entry to kotti.configurators
in the .ini config file for your project:::

    kotti.configurators =
        ...
        kotti_navigation.kotti_configure

Here are the slots available for the navigation widget:::

    left
    right
    abovecontent
    belowcontent
    belowbodyend

which you set with a config parameter:::

    kotti_navigation.navigation_widget.slot = abovecontent

.. Note:: Configure navigation for only one slot.

Here are the slot choices in a layout diagram:::

    +------------------------------------------------------+
    | nav (the nav in the Kotti toolbar -- configurable)   |
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

Configuring to Replace Top Nav
------------------------------

You see the top nav position in the diagram above (it is not a slot), where
default Kotti puts the nav.pt template. kotti_navigation provides a nav.pt
that can replace Kotti's nav.pt:::

    kotti_navigation/kotti-overrides/templates/view/nav.pt

that can be enabled in your ini file with:::

    kotti.asset_overrides = kotti_navigation:kotti-overrides/

This will tell Kotti that you are selecting any templates that are defined
within kotti_navigation:kotti-overrides and which match Kotti's directory
structure for templates. 

This top position is not a slot, so make sure to omit the slot setting or to
set it as:::

    kotti_navigation.navigation_widget.slot = none

For this top position, you will probably want to configure these nav settings
as:::

    kotti_navigation.navigation_widget.display_type = list
    kotti_navigation.navigation_widget.show_context_menu = true

and you probably want to omit the label setting. The breadrumbs may in this
usage be deemed redundant. If so, override Kotti's master template to omit it
(See below, under discussion of display_type).

The default development.ini config file has a tree nav in the left slot. See
the alternate top.ini for an example of a configuration replacing nav.pt.

Excluding the Root
------------------

To exclude the root of the site from the navigation, in either the tree
display or the context menu of the list display, set this:::

    kotti_navigation.navigation_widget.include_root = false

Excluding Content Types
-----------------------

You can exclude specific content types from the whole navigation
structure. If you not want to show images in the navigation at all,
set the ``kotti_navigation.navigation_widget.exclude_content_types`` 
variable to the following:::

    kotti_navigation.navigation_widget.exclude_content_types = 
        kotti.resources.Image
        kotti_myaddon.resources.MyContentType

Setting Display Type
--------------------

Control the type of display with the display_type setting, which can be either
``list`` (default) or ``tree``:::

    kotti_navigation.navigation_widget.display_type = list

Configuring the ``tree`` display is straightforward; you have the choice of
including the root, or not. The navigation tree shows the full site content in
an indented vertical list. When an item with children is clicked, it is
exploded, and with another item is clicked, it is collapsed. The tree display
is most appropriate for the left and right slots, but can be used in any other
slot, probably accompanied by customization through CSS.

The ``list`` display does not show the full site content; Only the
immediate children for the context are shown as a simple list of
navpills wrapped within the available space. This navigation menu can be used
in two ways, regarding the breadcrumbs display in default Kotti:

* Turn off the context menu for the ``list`` display with ``show_context_menu``
  set to false, and use Kotti's breadcrumbs display for providing essential
  navigation back up the site hierarchy
* Turn on the context menu fo the ``list`` display, and turn off Kotti's
  breadcrumbs display by overriding via templates. The context menu will
  provide an active link to go up one level from the current context, and will
  provide links to the root and top-level content items.

The ``list`` style of display is different for "horizontal" vs. "vertical"
aspect slots, as follows:

* In the abovecontent, belowcontent, and belowbodyend slots ("horizontal"
  aspect), the ``list`` display is akin to the display of tags as nav pills
  wrapping horizontally within a container filling the slot, plus a label
  and/or context menu item button if they are configured to be present.
* In the left and right slots, the ``list`` display is the nav-list style from
  Bootstrap, which shows items in a more traditional "vertical aspect" list
  format.

.. Note:: Regarding the default top nav-bar in Kotti, to avoid redundancy, you
          may want to override the nav.pt view template, or remove it from
          master.pt, so that there are no nav items shown in the top bar.

Configuring a Label
-------------------

There is an optional label for the top of the tree display, underneath the
context menu if it is enabled, or for the first item in the list display.

For the following discussion about the optional label, the context is assumed
to be a document titled Animals, and there are two children titled Dogs and
Cats.

**A label for a tree display**

The optional label at the top of the tree dislay would usually be set to
``none``, because the nature of the indentation should make the context
obvious. In some situations, however, a simple label such as "Site Navigation"
or "Site Menu" could be desired. To set such a label, do:::

    kotti_navigation.label = Site Menu

.. Note:: String params in ini config files do not have quotes, so the string
          is whatever comes after the = sign, with leading whitespace deleted.

The current context will be indicated by the highlighting of the context menu
item in the tree display. This is normally adequate. However, for extra
clarity, or for some special reason, you may want to include the current
context in the label, in a phrase such as "Current item: context", where the
word ``context`` would be replaced by the actual context.title, e.g.  "Current
item: Cats". So, include the actual word ``context`` in the label text:::

    kotti_navigation.label = <context>

(the label would become ${'<' + context.title '>'} in the template code, which
would become ``<Animals>`` in the rendered label.)

Or, if the site's ``breadcrumbs`` display is not shown, by overriding
templates, and you want to have a simple replacement in concert with the tree
display, do:::

    kotti_navigation.label = You are here: context

(``You are here: Animals``).

**A label for a list display**

If using a list display for navigation, the default will list children of the
current context in a list of nav pills that wrap, if necessary. Along with the
default Kotti nav toolbar and and breadcrumbs, this may provide a perfectly
good nav display.  When the abovecontent slot is used, however, the title for
the context is _underneath_ the nav list, so it may not be clear enough that
that the nav pill items are children within the context.  Perhaps this would
be true for the left slot, as well, but a bare nav pill list in the right and
belowcontent slots might work well.

If label is not set, the default value of none will result in two nav pill li
items for the example Animals context:::

    <Dogs> <Cats>
    
(< > notation used here to denote nav pill li items).

Using a custom string, punctuated with a colon:::

    kotti_navigation.label = Contained Items:

would result in a nav-header styled label with two nav pill li items, as:::

    Contained items: <Dogs> <Cats>

or, perhaps with some other punctuation:::

    kotti_navigation.label = Contents >>

etc.

As described above, set label to a string using the word ``context`` anywhere
in the string as a placeholder for context.title.

    kotti_navigation.label = context

The result would be a label for Animals and two nav pill li items, as:::

    Animals <Dogs> <Cats>

With any punctuation or additional text of any sort along with context in the
label, as with:::

    label = context:

becomes:::

    Animals: <Dogs> <Cats>

If a phrase is used, take care to word appropriately, perhaps aided by use of
quotes or another indicator for context, such as (), [], etc.:::

    kotti_navigation.label = Items in [context] are:::

would result in:::

    Items in [Animals] are: <Dogs> <Cats>

and:::

    kotti_navigation.label = "context" contains:

would result in:::

    "Animals" contains: <Dogs> <Cats>

etc.

Configuring for Use with a Menu System
--------------------------------------

To open the whole navigation all the time, set the ``open_all`` variable. This
is useful if you plan to set up a popup menu via css or javascript:::

    kotti_navigation.navigation_widget.open_all = false

You will want to set display_type to ``tree``, because the ``list``
shows, by design, only the children of the current context. The ``tree``
display, when open_all is true, will produce items for each node in the full
tree.

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

