from setuptools import setup
from setuptools import find_packages

requirements = ['numpy',
                'netCDF4 == 1.1.1',
                'pyresample',
                'pyyaml',
                'pillow']

readme_contents = open('README.md', 'r').read()

setup(
      name='Satistjenesten',
      author='Mikhail Itkin',
      description='Istjenesten satellite processing suite',
      long_description=readme_contents,
      install_requires=requirements,
      test_suite='tests',
      )
