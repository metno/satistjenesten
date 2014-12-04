from setuptools import setup

requirements = ['sphinxcontrib-napoleon', 'mock']
requires = ['numpy', 'pyresample', 'netCDF4']
test_requires=["mock"]
setup(name='satistjenesten',
        packages=['satistjenesten', 'satistjenesten'],
        package_dir={'satistjenesten': 'satistjenesten'},
        author='Mikhail Itkin',
        install_requires=requirements,
        description='resampler and netcdf IO')
extras_require = {'nc': 'netCDF4'}
