from setuptools import setup

setup(name='src-stats',
      version='0.1',
      package_dir={'': 'src'},
      packages=['srcstats'],
      test_suite='nose.collector',
      entry_points={
          'console_scripts': [
              'count-lines = srcstats.countlines_cmd:main_func']})
