from setuptools import setup, find_packages
import os


version = '0.2'
project = 'kotti_navigation'


tests_require = [
    'WebTest',
    'mock',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'wsgi_intercept',
    'zope.testbrowser',
    ]


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('docs', 'THANKS.txt')
    + '\n' +
    read('docs', 'CHANGES.txt'))


setup(name=project,
      version=version,
      description="""Add a configurable navigation to your Kotti site""",
      long_description=long_description,
      classifiers=[],
      keywords='kotti addon',
      author='Marco Scheidhuber',
      author_email='j23d@jusid.de',
      url='http://pypi.python.org/pypi/kotti_navigation',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Kotti>=0.7a3',
      ],
      tests_require=tests_require,
      entry_points="""
      [fanstatic.libraries]
      kotti_navigation = kotti_navigation:library
      """,
      extras_require={
          'testing': tests_require,
          },
      message_extractors={'kotti_navigation': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )
