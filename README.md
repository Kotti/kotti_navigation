# kotti_navigation

This is an extension to the [Kotti CMS][1] that renders navigation displays in a
choice of available locations for a Kotti website (top nav, left slot, right
slot).


## Set up kotti_navigation

To activate kotti_navigation add the following entry, as with any add-on, to
kotti.configurators of your .ini config file. ``kotti_navigation`` depends on
[kotti_settings][2], so you have to add also an entry for this add-on. So the
kotti.configurators part of your your ini file should include the following
lines.

```ini
kotti.configurators =
    ...
    kotti_navigation.kotti_configure
    kotti_contentpreview.kotti_configure
```

## How to use it?

You have different settings to adjust ``kotti_navigation`` to your needs. You
get the settings page on http://yourkottidomain.tdl/@@settings and you find it
a link to `Settings` in the dropdown of menupoint `Administrator` of the editor
bar. In the default no special navigation is activated and the default navigation
bar from Kotti will be used.


![settings](https://raw.github.com/Kotti/kotti_navigation/master/docs/images/settings.png "Navigation Settings")

There are three locations are available::

* top (within and beneath the default nav toolbar)
* left (slot)
* right (slot)

For every location you have an own tab in the settings. There you can choose
if the navigation is enabled for the location and how it will be displayed.
The following options are available.

### Display Types

With the display type you choose how your navigation will be rendered.

- Not enabled
  > As expected the widget will not be shown in the slot.
- Tree
  > The full tree is used for the navigation.
- Items
  > Only the the children of the current context are included.
- Menu
  > The navigation will be rendered as a dropdown menu.
- Breadcrumbs
  > Here the real breadcrumbs will be rendered, useful when you need it
    in another slot than usual.

For a typical website that has a tree navigation display in the left slot, you
would configure for only the left location, and omit configuration for any
other. But you are encouraged to play around with the possibilities.

### Options

The options are a multi selection box, so you can enable how much you want, however
it will not always make sense to mix all of the options together.

- List
- Pills
- Tabs
  > These define the bootstrap classes that are used to render the navigation. It is
    recommended to only use one of them.
- Stacked
  > This makes your navigation stackable. Refer to the [bootstrap documentation](http://getbootstrap.com/components/#nav) for more information.
- Open all
  > This will be open all of your menu points no matter where your context is. This is
    useful if you plan to set up a menu via css or javascript, because all items in the
    site hierarchy are always included.
- With Dropdowns
  > tbd
- Show Menu
  > tbd
- Include Root
  > Indicate if the root object will be included on the top of the navigation and so an item
    showing the title of the root of the site is inserted as the first item for the display
    choices.
- Show hidden while logged in
  > With this option enabled items that are not included in the navigation for the user
    of the website are shown to the editor or admin.


### Include Content Types

Here you find a list of the content type names that are to be allowed in a given navigation
display. Use this, for example, to have a nav tabs display in the top location, along with
an images-only display in the right slot. The images-only nav display could be given a label
such as "Images:" for clarity.

### Exclude Content Types

This is a list of the names of content types that are to be ignored in the navigation
display. It is the opposite of the ``Include Content Types`` setting described above. It is
commonly used to exclude the Image content type from a normal nav display, to avoid the
"clutter" with listing images, which can be numerous. The same could be true
for other content items, such as for a site that allows the Event content type
of kotti_calendar to be stored in various places in the site, and where events
are wished to be shown only on calendar or event list displays.

### Label

The label is optional, but can provide clarification in some nav display cases.
It is positioned within the display in different ways, depending on display
type. In a tree-type display (one of the "stacked" display choices), it is at
the top of the display. In a ver_list display, it is put underneath the context
menu button if it is enabled (with show_menu = True), or it is the first item.
In a "horizontal aspect" list display, it comes after the context menu button,
if enabled, or is the first item.

The label is optional, but can provide clarification in some nav display cases.
It is positioned within the display in different ways, depending on display
type. In a tree-type display (one of the "stacked" display choices), it is at
the top of the display. In a ver_list display, it is put underneath the context
menu button if it is enabled (with show_menu = True), or it is the first item.
In a "horizontal aspect" list display, it comes after the context menu button,
if enabled, or is the first item.

For the following discussion about the optional label, the context is assumed
to be a document titled Animals, and there are two children titled Dogs and
Cats.

**A label for a Tree-like ("stacked") display**

The optional label at the top of a dislay of this type would usually be
omitted, because the nature of the indentation should make the context
apparent. In some situations, however, a simple label such as "Site Navigation"
or "Site Menu" could be desired. To set such a label, do::

    Site Menu

.. Note:: String params in ini config files do not have quotes, so the string
          is whatever comes after the = sign, with leading whitespace deleted.

The current context will be indicated by the highlighting of the context menu
item in the indented display. This is normally adequate. However, for extra
clarity, or for some special reason, you may want to include the current
context in the label, in a phrase such as "Current item: context", where the
word ``context`` would be replaced by the actual context.title, e.g.  "Current
item: Cats". To do this, include the actual word ``context`` in the label
text::

    kotti_navigation.navigation_widget.left_label = <context>

(the label would become ${'<' + context.title '>'} in the template code, which
would become ``<Animals>`` in the rendered label.)

Or, to provide a breadcrumbs-style label, do::

    kotti_navigation.navigation_widget.left_label = You are here: context

(``You are here: Animals``).

**A label for a horizontal list type display**

If using a "horizontal aspect" list display for navigation, the default will
list children of the current context in a list of nav items that wrap, if
necessary. If present along with a breadcrumbs display, this may provide a
perfectly good navigation display.  When the abovecontent slot location is
used, however, the title for the context, along with the body content, is
_underneath_ the nav list, so it may not be clear enough that that the nav
items are children within the context.  Perhaps this would be true for the left
slot, as well, but a bare nav item list in the right and belowcontent slots
might work fine.

For the "Animals" context, if label is not set, there will be two nav items::

    <Dogs> <Cats>

(< > notation used here to denote nav li items).

Using a label, punctuated with a colon, we might have::

    kotti_navigation.navigation_widget.left_label = Contained Items:

This would result in a nav-header styled label with two li items, as::

    Contained items: <Dogs> <Cats>

or, perhaps some other punctuation could be used instead of a colon::

    kotti_navigation.navigation_widget.left_label = Contents >>

etc.

As described above, use the word ``context`` anywhere in the label text as a
placeholder for context.title. Used alone::

    kotti_navigation.navigation_widget.left_label = context

the result would be a label for Animals and two nav li items::

    Animals <Dogs> <Cats>

Again, punctuation or additional text may help, as with::

    kotti_navigation.navigation_widget.left_label = context:

which becomes::

    Animals: <Dogs> <Cats>

If a phrase is used, take care to word appropriately, perhaps aided by use of
an additional indication for context, such as (), [], etc.::

    kotti_navigation.navigation_widget.left_label = Items in [context] are::

which would result in::

    Items in [Animals] are: <Dogs> <Cats>

and::

    kotti_navigation.navigation_widget.left_label = "context" contains:

would result in::

    "Animals" contains: <Dogs> <Cats>

etc.


[1]:  http://pypi.python.org/pypi/Kotti
[2]: http://pypi.python.org/pypi/kotti_settings
