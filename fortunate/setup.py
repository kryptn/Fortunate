from setuptools import setup

setup(name='fortunate',
      packages=['fortunate'],
      include_package_data=True,
      install_requires=['flask',
                        'flask-sqlalchemy',
                        'flask-testing',])

