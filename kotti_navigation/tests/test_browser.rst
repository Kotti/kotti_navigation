kotti_navigation browser tests
==============================

Setup and Login
---------------

  >>> from kotti import testing
  >>> tools = testing.setUpFunctional(
  ...     **{'kotti.configurators': 'kotti_navigation.kotti_configure',
  ...        'kotti_navigation.navigation_widget.include_root': 'true',
  ...        'kotti_navigation.navigation_widget.open_all': 'true',
  ...        'kotti_navigation.navigation_widget.show_hidden_while_logged_in': 'true',
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
  >>> 'Successfully added item' in browser.contents
  True
  >>> browser.open(testing.BASE_URL + '/document-1/@@add_document')
  >>> ctrl('Title').value = 'Document 1 1'
  >>> ctrl('Description').value = 'This is the second document'
  >>> ctrl('save').click()


Check navigation
----------------

  >>> browser.open(testing.BASE_URL)
  >>> 'Document 1 1' in browser.contents
  True


Test hidden nav points
----------------------

  >>> browser.open(testing.BASE_URL)
  >>> browser.getLink('Contents').click()
  >>> childs = ctrl(name='children')
  >>> childs.value = childs.options[0:1]
  >>> ctrl(name='hide').click()
  >>> "Document 1 is no longer visible in the navigation" in browser.contents
  True
  >>> browser.open(testing.BASE_URL)
  >>> 'Document 1' in browser.contents
  True
  >>> 'hidden' in browser.contents
  True
  >>> browser.open(testing.BASE_URL + '/logout')
  >>> browser.open(testing.BASE_URL)
  >>> 'Document 1' in browser.contents
  False
  >>> 'hidden' in browser.contents
  False
