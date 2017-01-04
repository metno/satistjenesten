from setuptools import setup
from setuptools import find_packages
import os

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
      packages=['satistjenesten'],
      data_files=[os.path.join(os.path.dirname(__file__), 'test_data', 'DroidSans.ttf')],
      long_description=readme_contents,
      install_requires=requirements,
      test_suite='tests',
      scripts=['scripts/amsr2_mosaic.py',  'scripts/mitiff2geotiff.py',  'scripts/mitiff_mosaic.py'],
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
