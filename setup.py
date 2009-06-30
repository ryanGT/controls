from distutils.core import setup
setup(name='controls',
      version='1.0',
      description='A Python module for system dynamics and feedback control analysis of linear, time invariant systems',
      author='Ryan Krauss',
      author_email='ryankrauss@gmail.com',
      packages=['controls'],
      package_dir={'controls': 'src/controls'},
      package_data={'controls': ['examples/*.py']},
      )
