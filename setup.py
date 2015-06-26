from setuptools import setup
from setuptools import find_packages

requirements = ['numpy',
                'netCDF4',
                'pyresample',
                'pyyaml',
                'pillow',
                'rasterio']

readme_contents = ""

setup(
      name='satistjenesten',
      version=0.5,
      author='Mikhail Itkin',
      description='Istjenesten satellite processing suite',
      long_description=readme_contents,
      install_requires=requirements,
      test_suite='tests',
      # packages=find_packages(exclude='tests'),
      packages=['satistjenesten'],
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Programming Language :: Python',
      'Operating System :: OS Independent',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering'
      ],
      include_package_data = True,
      )
