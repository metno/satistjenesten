from setuptools import setup

requirements = ['sphinxcontrib-napoleon']
requires = ['numpy', 'pyresample', 'netCDF4']
setup(name='satistjenesten',
        packages=['satistjenesten', 'satistjenesten.data', 'satistjenesten.retrievals',
                  'satistjenesten.utils'],
        package_dir={'satistjenesten': 'satistjenesten'},
        author='Mikhail Itkin',
        install_requires=requirements,
        description='resampler and netcdf IO')
extras_require = {'nc': 'netCDF4'}
