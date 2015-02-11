kotti_navigation browser tests
==============================

Setup and Login
---------------

  >>> from kotti import testing
  >>> from kotti_navigation.tests import set_nav_setting
  >>> tools = testing.setUpFunctional(
  ...     **{'kotti.configurators': 'kotti_navigation.kotti_configure'})
  >>> browser = tools['Browser']()
  >>> ctrl = browser.getControl

  >>> browser.open(testing.BASE_URL + '/@@login')
  >>> 'Log in' in browser.contents
  True
  >>> ctrl('Username or email', index=0).value = 'admin'
  >>> ctrl('Password', index=0).value = 'secret'
  >>> ctrl(name='submit').click()
  >>> 'Welcome, Administrator' in browser.contents
  True


Add some documents
------------------

  >>> browser.open(testing.BASE_URL + '/@@add_document')
  >>> ctrl('Title').value = 'Document 1'
  >>> ctrl('Description').value = 'This is the first document'
  >>> ctrl('save').click()
  >>> browser.url == testing.BASE_URL + '/document-1/'
  True
  >>> browser.open(testing.BASE_URL + '/document-1/@@add_document')
  >>> ctrl('Title').value = 'Document 1 1'
  >>> ctrl('Description').value = 'This is the second document'
  >>> ctrl('save').click()


Check navigation
----------------

  >>> set_nav_setting('top', 'display_type', 'tree')
  >>> set_nav_setting('top', 'options', ['list', 'show_menu', 'show_hidden_while_logged_in', 'include_root'])
  >>> set_nav_setting('top', 'label', 'Vertical List up Top')
  >>> browser.open(testing.BASE_URL + '/document-1')
  >>> 'Vertical List up Top' in browser.contents
  True


TearDown
--------

  >>> testing.tearDown()
