from setuptools import setup
from setuptools import find_packages
from setuptools_behave import behave_test

requirements = ['numpy',
                'netCDF4',
                'pyresample',
                'pyyaml']

test_requirements = ['nose',
                     'behave>=1.2.4']

readme_contents = open('README.md', 'r').read()

setup(
      name='AVHRR-meltponds',
      author='Mikhail Itkin',
      description='Melt ponds fraction retrieval',
      long_description=readme_contents,
      install_requires=requirements,
      tests_require=test_requirements,
      test_suite='tests',
      cmdclass={'behave_test': behave_test,}
      )
