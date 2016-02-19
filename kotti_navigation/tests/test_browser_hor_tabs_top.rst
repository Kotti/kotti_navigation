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


Set settings and check navigation
---------------------------------

  >>> browser.open(testing.BASE_URL + '/document-1')
  >>> 'id="navigation-list"' in browser.contents
  False
  >>> '<ul class="nav nav-pills">' in browser.contents
  False


  >>> set_nav_setting('top', 'display_type', 'items')
  >>> set_nav_setting('top', 'display_manner', 'pills')
  >>> set_nav_setting('top', 'label', 'Horizontal Tabs up Top')
  >>> browser.open(testing.BASE_URL + '/document-1')
  >>> 'Horizontal Tabs up Top' in browser.contents
  True
  >>> 'id="navigation-list"' in browser.contents
  True
  >>> '<ul class="nav nav-pills">' in browser.contents
  True

  >>> set_nav_setting('top', 'display_manner', 'tabs')
  >>> browser.open(testing.BASE_URL + '/document-1')
  >>> '<ul class="nav nav-pills">' in browser.contents
  False
  >>> '<ul class="nav nav-tabs">' in browser.contents
  True


TearDown
--------

  >>> testing.tearDown()
