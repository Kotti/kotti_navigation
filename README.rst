================
kotti_navigation
================

This is an extension to the Kotti CMS that renders a navigation in one of the
available locations for a Kotti website (top nav, left slot, right slot,
abovecontent slot, etc.).

`Find out more about Kotti`_

Setting up the navigation widget
================================

To activate kotti_navigation you must add the following entry, as with any
add-on, to kotti.configurators of your .ini config file:::

    kotti.configurators =
        ...
        kotti_navigation.kotti_configure

The default configuration will add no navigation display, and it will remove
the default Kotti navbar in the top position, so you MUST configure for at
least one location, unless you are using kotti_navigation, ironically, to
purposefully turn off Kotti's default top navigation (Kotti's default
breadcrumbs would be the only navigation available).

Location
--------

Six locations are available for the navigation widget:::

    top (within the default nav toolbar)
    left (slot)
    right (slot)
    abovecontent (slot)
    belowcontent (slot)
    belowbodyend (slot)

They can be used in any combination.

Here are the location choices (in all-caps) in a layout diagram:::

    +------------------------------------------------------+
    | "top" (This is the top toolbar; not a real slot.     |
    |        kotti_navigation changes it to be only the    |
    |        brand at left and search at right. Some       |
    |        nav display choices are available for the     |
    |        space between branch and search, and below    |
    |        the div for the top nav bar, in a separate    |
    |        div.                                          | 
    |------------------------------------------------------|
    | editor_bar                                           |
    |+----------------------------------------------------+|
    || breadcrumbs (This is Kotti's default breadcrumbs.  ||
    ||              Depending on how you configure        ||
    ||              kotti_navigation, you may want to     ||
    ||              turn this off by overriding           ||
    ||              master.pt in kotti_overrides).        ||
    |+-------------++---------------------++--------------+|
    || slot "left" || slot "abovecontent" || slot "right" ||
    ||             |+---------------------+|              ||
    ||             || Content             ||              ||
    ||             |+---------------------+|              ||
    ||             || slot "belowcontent" ||              ||
    |+-------------++---------------------++--------------+|
    | footer (Kotti's; not removed).                       |
    |------------------------------------------------------|
    | slot "beforebodyend"                                 |
    +------------------------------------------------------+

Each of these locations can be separately configured to have one or more
navigation displays. The display type and other options for a given location
are configured with lines like these:::

    kotti_navigation.navigation_widget.left_display_type = ver_pills_stacked
    kotti_navigation.navigation_widget.left_label = none
    kotti_navigation.navigation_widget.left_include_root = true
    ...
    ... additional params
    ...

For a site with NO navigation, you could omit all such configuration, except
for the kotti_navigation.kotti_configure line in kotti.configurators.

For a typical website that has a tree navigation display in the left slot,
you would configure for only the left location, and omit the others.

Display Types
-------------

There are five "horizontal aspect" and five "vertical aspect" navigation
display types available, and a menu dropped down from a single button:::

    Display Type                 Aspect                Items Shown
    ---------------------------  ----------            --------------------
    hor_tabs                     horizontal (items)    context children
    hor_pills                    horizontal (items)    context children
    hor_tabs_with_dropdowns      horizontal (items)    context children +1
    hor_pills_with_dropdowns     horizontal (items)    context children +1
    breadcrumbs                  horizontal (items)    path to context
    ver_tabs_stacked             vertical (tree-like)  context children
    ver_pills_stacked            vertical (tree-like)  context children
    ver_tabs_stacked_open_all    vertical (tree-like)  entire hierarchy
    ver_pills_stacked_open_all   vertical (tree-like)  entire hierarchy
    ver_list                     vertical (items)      context children
    menu                         button with caret     path to context +1
                                 firing dropdown menu

Terminology
-----------

The names of Bootstrap styles are used directly for display types, because this
is more explicit than use of the terms "tree" and "list", which for Bootstrap
can be confusing.

Any of the display types having "stacked" in the name are tree-like, and have a
vertical aspect, consisting of items shown one under the other, indented to
show the hierarchy: ver_tabs_stacked, ver_pills_stacked,
ver_tabs_stacked_open_all, and ver_pills_stacked_open_all.

The ``open_all`` choices are useful if you plan to set up a popup menu via css
or javascript, because all items in the site hierarchy are always included.

ver_list is also vertical aspect, but this uses the specific nav-list CSS style
of Bootstrap, vs. ver-tabs and ver-pills used for the "stacked" choices.

All of the display types listed above as having a horizontal aspect consist of
items shown one after another, from left to right, in a row-fluid style
display.

The menu consists of a button with a caret, that fires a dropdown display
useful on its own as a complete navigation solution. It can be used in
combination with some of the other display types as a "context" menu, providing
a general site and indented context list, analagous to the "You are here"
information in breadcrumbs. 

The breadcrumbs display type is exactly the one used in default Kotti, showing
items in the path (in the lineage) as links in a horizontal list, delimited by
the "/" character, and ending in an item for the current context. With this
breadcrumbs display, however, you can control the label. If you configure
kotti_navigation's breadcrumbs display, you may wish to override the one in
default Kotti, by adding a modified master.pt to the kotti-overrides directory.

Configuration for Display Types
-------------------------------

You can have multiple navigation displays -- you can configure navigation in
all six locations at the same time if you want, but usually one or two will do
fine!

For each location, these configuration settings are available, given the
restrictions on display type described above:::

    kotti_navigation.navigation_widget.left_display_type = ver_pills_stacked
    kotti_navigation.navigation_widget.left_show_menu = false
    kotti_navigation.navigation_widget.left_label = none
    kotti_navigation.navigation_widget.left_include_root = true
    kotti_navigation.navigation_widget.left_include_content_types = (e.g., Image)
    kotti_navigation.navigation_widget.left_exclude_content_types = (e.g., Image)
    kotti_navigation.navigation_widget.left_show_hidden_while_logged_in = true

(Substitute any another location name for "left" in these settings.)

If show_menu is True, a button which fires the menu dropdown will be shown as
the first item in either a horizontal or vertical aspect display of items.

If label is not none, it will be shown as the first item, or as the second, if
show_menu is True.

If include_root is True, an item showing the title of the root of the site is
inserted as the first item.

include_content_types is a list of the content type names that are to be
allowed in a navigation display. Use this, for example, to show only Images in
a nav display, along with a label "Images:", in combination with a normally
configured nav (Imagine a nav tabs display in the top location, along with an
images-only display in the right slot). This setting is separate from the Kotti
general content property ``in_navigation``, a boolean associated with the
"Show/Hide" toggle available for individual content items in the Contents menu.
Entries for include_content_types have the full path:::

    kotti_navigation.navigation_widget.include_content_types = 
        kotti.resources.Image
        kotti_myaddon.resources.MyContentType

exclude_content_types is a list of the content type names that are to be
ignored in the navigation displays. It is the opposite of the ``include``
setting described above. It is commonly used to exclude the Image content type
from a normal nav display, to avoid the "clutter" with listing images, which
can be numerous. 

show_hidden_while_logged_in offers an admin user the choice of viewing hidden
items (for which in_navigation is toggled OFF), for use in simpifying editing.

Kotti's Default Top Nav
-----------------------

In a default Kotti website, there is a bare-bones display of top-level content
items in what is labeled above as the "TOP" position (the top nav bar, that has
the brand on the left and a search input on the right). This would be redundant
and perhaps confusing if used in combination with kotti_navigation, so it is
overridden completely, by replacing the nav.pt template.  Find
kotti_navigation's version in:::

    kotti_navigation/kotti-overrides/templates/view/nav.pt

This template is used in combination with the other kotti_navigation templates,
which you find in kotti_navigation/templates/.

Configuring a Label
-------------------

There is an optional label. It appears in different ways, depending on display
type. In a tree, it is at the top of the tree display. In a "vertical aspect"
list, in the left or right slot, it is underneath the context menu if it is
enabled, or it is the first item in the list display. In a "horizontal aspect"
list display, it comes after the context menu, if enabled, or is the first
item.

For the following discussion about the optional label, the context is assumed
to be a document titled Animals, and there are two children titled Dogs and
Cats.

**A label for a tree display**

The optional label at the top of the tree dislay would usually be set to
``none``, because the nature of the indentation should make the context
obvious. In some situations, however, a simple label such as "Site Navigation"
or "Site Menu" could be desired. To set such a label, do:::

    kotti_navigation.navigation_widget.left_label = Site Menu

.. Note:: String params in ini config files do not have quotes, so the string
          is whatever comes after the = sign, with leading whitespace deleted.

The current context will be indicated by the highlighting of the context menu
item in the tree display. This is normally adequate. However, for extra
clarity, or for some special reason, you may want to include the current
context in the label, in a phrase such as "Current item: context", where the
word ``context`` would be replaced by the actual context.title, e.g.  "Current
item: Cats". So, include the actual word ``context`` in the label text:::

    kotti_navigation.navigation_widget.left_label = <context>

(the label would become ${'<' + context.title '>'} in the template code, which
would become ``<Animals>`` in the rendered label.)

Or, if the site's ``breadcrumbs`` display is not shown, by overriding
templates, and you want to have a simple replacement in concert with the tree
display, do:::

    kotti_navigation.navigation_widget.left_label = You are here: context

(``You are here: Animals``).

**A label for a list display**

If using a "horizontal aspect" list display for navigation, the default will
list children of the current context in a list of nav pills that wrap, if
necessary. Along with the default Kotti nav toolbar and and breadcrumbs, this
may provide a perfectly good nav display.  When the abovecontent slot is used,
however, the title for the context is _underneath_ the nav list, so it may not
be clear enough that that the nav pill items are children within the context.
Perhaps this would be true for the left slot, as well, but a bare nav pill list
in the right and belowcontent slots might work well.

If label is not set, the default value of none will result in two nav pill li
items for the example Animals context:::

    <Dogs> <Cats>
    
(< > notation used here to denote nav pill li items).

Using a custom string, punctuated with a colon:::

    kotti_navigation.navigation_widget.left_label = Contained Items:

would result in a nav-header styled label with two nav pill li items, as:::

    Contained items: <Dogs> <Cats>

or, perhaps with some other punctuation:::

    kotti_navigation.navigation_widget.left_label = Contents >>

etc.

As described above, set label to a string using the word ``context`` anywhere
in the string as a placeholder for context.title:::

    kotti_navigation.navigation_widget.left_label = context

The result would be a label for Animals and two nav pill li items, as:::

    Animals <Dogs> <Cats>

With any punctuation or additional text of any sort along with context in the
label, as with:::

    kotti_navigation.navigation_widget.left_label = context:

becomes:::

    Animals: <Dogs> <Cats>

If a phrase is used, take care to word appropriately, perhaps aided by use of
quotes or another indicator for context, such as (), [], etc.:::

    kotti_navigation.navigation_widget.left_label = Items in [context] are:::

would result in:::

    Items in [Animals] are: <Dogs> <Cats>

and:::

    kotti_navigation.navigation_widget.left_label = "context" contains:

would result in:::

    "Animals" contains: <Dogs> <Cats>

etc.

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
