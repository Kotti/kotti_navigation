from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('THANKS.txt')
    + '\n' +
    read('CHANGES.txt'))


setup(name='kotti_navigation',
      version='0.3a1',
      description="""Add a configurable navigation to your Kotti site""",
      long_description=long_description,
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: Repoze Public License',
      ],
      keywords='kotti addon navigation',
      author='Marco Scheidhuber',
      author_email='j23d@jusid.de',
      url='http://pypi.python.org/pypi/kotti_navigation',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Kotti>=0.8a1',
      ],
      tests_require=[],
      entry_points="""
      [fanstatic.libraries]
      kotti_navigation = kotti_navigation:library
      """,
      extras_require={},
      message_extractors={'kotti_navigation': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )
