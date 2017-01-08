from setuptools import setup

setup(name='fortunate',
      packages=['fortunate'],
      include_package_data=True,
      test_suite='fortunate.tests',
      install_requires=['flask',
                        'flask-sqlalchemy',
                        'flask-testing',
                        'psycopg2'])

