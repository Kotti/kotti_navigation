kotti_navigation browser tests
==============================

Setup and Login
---------------

  >>> from kotti import testing
  >>> tools = testing.setUpFunctional(
  ...     **{'kotti.configurators': 'kotti_navigation.kotti_configure',
  ...        'kotti_navigation.navigation_widget.top_display_type': 'menu',
  ...        'kotti_navigation.navigation_widget.top_include_root': 'false',
  ...        'kotti_navigation.navigation_widget.top_include_content_types': 'kotti.resources.Document',
  ...        'kotti_navigation.navigation_widget.top_show_hidden_while_logged_in': 'true',
  ...       })
  >>> browser = tools['Browser']()
  >>> ctrl = browser.getControl

  >>> browser.open(testing.BASE_URL + '/@@login')
  >>> 'Log in' in browser.contents
  True
  >>> ctrl('Username or email').value = 'admin'
  >>> ctrl('Password').value = 'secret'
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

  >>> browser.open(testing.BASE_URL + '/document-1/document-1-1')
  >>> '&lt;&lt; Document 1' in browser.contents
  True
