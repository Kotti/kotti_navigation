kotti_navigation browser tests
==============================

Setup and Login
---------------

  >>> from kotti import tests
  >>> tools = tests.setUpFunctional(
  ...     **{'kotti.configurators': 'kotti_navigation.kotti_configure',
  ...        'kotti_navigation.navigation_widget.include_root': 'true',
  ...        'kotti_navigation.navigation_widget.levels': '3',
  ...       })
  >>> browser = tools['Browser']()
  >>> ctrl = browser.getControl

  >>> browser.open(tests.BASE_URL + '/@@login')
  >>> "Log in" in browser.contents
  True
  >>> ctrl("Username or email").value = "admin"
  >>> ctrl("Password").value = "secret"
  >>> ctrl(name="submit").click()
  >>> "Welcome, Administrator" in browser.contents
  True


Add some documents
------------------

  >>> browser.open(tests.BASE_URL + '/@@add_document')
  >>> ctrl("Title").value = "Document 1"
  >>> ctrl("Description").value = "This is the first document"
  >>> ctrl("save").click()
  >>> browser.url == tests.BASE_URL + '/document-1/'
  True
  >>> "Successfully added item" in browser.contents
  True
  >>> browser.open(tests.BASE_URL + '/document-1/@@add_document')
  >>> ctrl("Title").value = "Document 1 1"
  >>> ctrl("Description").value = "This is the second document"
  >>> ctrl("save").click()


Check navigation
----------------

  >>> browser.open(tests.BASE_URL)
